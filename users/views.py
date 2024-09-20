# users/views.py
import urllib
import json

from django.views.generic import ListView, TemplateView, UpdateView, CreateView
from django.conf import settings

from django.urls import reverse_lazy
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect, get_object_or_404

from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.db.models import Q

from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.http import Http404

from .tokens import account_activation_token

from django.http import JsonResponse, HttpResponseRedirect


from django.contrib.auth import login
from .forms import CustomUserCreationForm
from .models import CustomUser, EmailListEntry, MassEmail


class UpdateAccount(UpdateView):
    model = CustomUser
    fields = ['first_name', 'last_name', 'email', 'organization', 'user_type']
    success_url = reverse_lazy('my_account')
    template_name = 'accounts/update_account.html'

    def get_object(self, queryset=None):
        '''This method will load the object
        that will be used to load the form
        that will be edited'''
        return self.request.user


def my_account(request):
    return render(request, 'accounts/my_account.html',)


def sign_up(request):
    """ User sign up for account.
    sign_up creates the User Sign Up view using the CustomUserCreationForm
    created in users/forms.py
    """
    # If the user submitted the form (i.e. 'POST')
    if request.method == 'POST':
        # then our form is our CustomUserCreationForm populated with the
        # user's submitted data
        form = CustomUserCreationForm(request.POST)
        # if the form is valid (i.e. it passes all of the validations for
        # each form field)
        if form.is_valid():
            # then save the form (but wait to commit it because we need
            # to set is_active to false for now so that the user can be
            # confirmed via email)
            user = form.save(commit=False)
            # set is_active to false
            user.is_active = False  # THIS SHOULD BE FALSE IN PRODUCTION!!
            # save the inactive user data
            user.save()
            # grab the domain name of our site to use in our email link
            current_site = get_current_site(request)
            # confirmation email subject
            subject = 'Activate Your PoPS Model Account'
            # create confirmation email message from our template and variables
            message = render_to_string('account_activation_email.html', {
                # get current user
                'user': user,
                # get current site domain
                'domain': current_site.domain,
                # create an encoded uid to use in the email confirmation link (
                # this encodes the user's primary key [user.pk]). When the user
                # clicks on the link, this value gets passed to
                # the activate view and decoded to determine the user.
                # 'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                # create a token to use in the email confirmation link. The
                # token is generated in users/tokens.py and is a combination
                # of the user's primary key and email_confirmed status. This
                # value is passed to activate view when user clicks on
                # the link.
                # After the email is confirmed, the activation link will no
                # longer work because the token will no longer be valid.
                'token': account_activation_token.make_token(user),
            })
            # email the user using their provided email address
            user.email_user(subject, message)
            # redirect user to account_activation_sent view
            return redirect('account_activation_sent')
    # If the request method is not a POST (i.e. the user hasn't submitted
    # data yet)
    else:
        # Then the form is our CustomUserCreationForm
        form = CustomUserCreationForm()
    # Return the signup form. If this is the first time it is rendered,
    # it will be blank. If the user has already attempted to fill out
    # the form, but it is invalid, then the form will be populated
    # with the user's content and error messages will be displayed
    return render(request, 'signup.html', {'form': form})


def account_activation_sent(request):
    # Show user a page saying that the account_activation email has been sent
    return render(request, 'account_activation_sent.html')


def activate(request, uidb64, token):
    """  When the user clicks on the account_activation link in their email,
    this is the view that they are directed to. It passes the UID and
    token that was created in the sign_up view.
    """
    try:
        # The uidb64 is the user's primary key encoded using the secret
        # key in settings. Try to decode it to get the user's pk.
        uid = urlsafe_base64_decode(uidb64).decode()
        # Get the user using the decoded primary key.
        user = CustomUser.objects.get(pk=uid)
    # If we can't get the user from the decoded primary key, set user to none.
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None
    # If the user exists (i.e. is not None), and the token for the user and
    # email_confirmed status checks out.
    if user is not None and account_activation_token.check_token(user, token):
        # Set user to active
        user.is_active = True
        # Set email_confirmed to true (this makes the token / email link no
        # longer work)
        user.email_confirmed = True
        # Save the is_active and email_confirmed fields to the user object
        user.save()
        # Go ahead and log the user in
        login(request, user)
        # Redirect to the desired page
        return redirect('workspace')
    # If the user and/or token do not work, direct the user to an invalid page
    else:
        return render(request, 'account_activation_invalid.html')


class UserListView(ListView):
    model = CustomUser


class SearchView(TemplateView):
    template_name = 'search_users.html'


class SearchResultsView(ListView):
    model = CustomUser
    template_name = 'search_results.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        object_list = CustomUser.objects.filter(
            Q(first_name__icontains=query) | Q(last_name__icontains=query)
        )
        return object_list


class AddNewEmail(CreateView):
    """ View for endusers to sign up for the listserve.
    If form is valid, saves the email to the EmailListEntry
    model and sends the user an email to confirm.
    """
    model = EmailListEntry
    template_name = "accounts/subscribe_email.html"
    fields = ['email']
    success_url = "subscribe_email"

    def form_invalid(self, form):
        print('Form invalid')
        response = super().form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response

    def form_valid(self, form):
        print('form_valid')
        self.object = form.save(commit=False)
        # We make sure to call the parent's form_valid() method because
        # it might do some processing (in the case of CreateView, it will
        # call form.save() for example).
        # Make any changes to form content before calling super.
        # form.instance.created_by = self.request.user
        #response = super().form_valid(form)
        ''' Begin reCAPTCHA validation '''
        recaptcha_response = self.request.POST.get('g-recaptcha-response')
        print(recaptcha_response)
        url = 'https://www.google.com/recaptcha/api/siteverify'
        values = {
            'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
            'response': recaptcha_response
        }
        data = urllib.parse.urlencode(values).encode()
        req =  urllib.request.Request(url, data=data)
        response = urllib.request.urlopen(req)
        print(response)
        result = json.loads(response.read().decode())
        print(result)
        ''' End reCAPTCHA validation '''
        email_object = self.object

        if result['success']:
            form.save()
            current_site = get_current_site(self.request)
            # confirmation email subject
            subject = 'Confirm your email for PoPS'
            email_object = self.object
            # create confirmation email message from our template and variables
            message = render_to_string('accounts/email_activation_email.html', {
                # get current site domain
                'domain': current_site.domain,
                # create an encoded uid to use in the email confirmation link (
                # this encodes the user's email. When the user
                # clicks on the link, this value gets passed to
                # the activate view and decoded to determine the email.
                'uid': urlsafe_base64_encode(force_bytes(email_object.pk)),
                # create a token to use in the email confirmation link. The
                # token is generated in users/tokens.py and is a combination
                # of the primary key and email_confirmed status. This
                # value is passed to activate view when user clicks on the link.
                # After the email is confirmed, the activation link will no longer
                # work because the token will no longer be valid.
                'token': account_activation_token.make_token(email_object),
            })
            send_mail(
                subject,
                message,
                "PoPS Model <noreply@popsmodel.org>",
                [email_object.email],
                fail_silently=False,
            )
        else:
            print('Recaptcha failed')


        if self.request.is_ajax():
            if result['success']:
                print('Response is ajax')
                data = {
                    'email': email_object.email,
                }
            else:
                data = {
                    'error': 'reCAPTCHA failed'
                }
            return JsonResponse(data)
        else:
            if result['success']:
                print('Response NOT ajax')
                return redirect('account_activation_sent')
            else:
                return redirect('subscribe_email_error')

class AddNewEmailError(AddNewEmail):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["error"] = 'reCAPTCHA failed'
        return context
    

class DeleteEmail(TemplateView):

    model = EmailListEntry
    template_name = "accounts/unsubscribe_email.html"

    def get(self, request, *args, **kwargs):
        print('This is a GET')
        try:
            uidb64_value = kwargs['uidb64']
            uid = urlsafe_base64_decode(uidb64_value).decode()
            email = EmailListEntry.objects.get(pk=uid)
            print(email)
        except (TypeError, ValueError, OverflowError,
                EmailListEntry.DoesNotExist):
            raise Http404("Email does not exist.")
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        print('This is a POST')
        email = request.POST.get('email')
        # Get email pk from the uidb64 encoded value
        # Check to see if that email exists in the list
        try:
            uidb64_value = kwargs['uidb64']
            uid = urlsafe_base64_decode(uidb64_value).decode()
            email_from_uidb = EmailListEntry.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError,
                EmailListEntry.DoesNotExist):
            raise Http404("Email does not exist.")
        # Get email from the user's entered email
        try:
            object_to_delete = EmailListEntry.objects.get(email=email)
        except ObjectDoesNotExist:
            object_to_delete = None
        # If object exists AND matches the uidb64 encoded object, then delete
        if (object_to_delete is not None and
                object_to_delete == email_from_uidb):
            object_to_delete.delete()
            return HttpResponseRedirect(reverse_lazy("unsubscribe_successful"))
        else:
            context = {"uidb64": kwargs["uidb64"],
                       "errors": "Email does not match."}
            return self.render_to_response(context)


def confirm_email(request, uidb64, token):
    """ When the user clicks on the account_activation link in
    their email, this is the view that they are directed to. It
    passes the UID and token that was created in the sign_up view.
    """
    try:
        # The uidb64 is the primary key encoded using the
        # secret key in settings.
        # Try to decode it to get the pk.
        uid = urlsafe_base64_decode(uidb64).decode()
        # Get the user using the decoded primary key.
        email = EmailListEntry.objects.get(pk=uid)
    # If we can't get the user from the decoded primary key, set user to none.
    except (TypeError, ValueError, OverflowError, EmailListEntry.DoesNotExist):
        email = None
    # If the user exists (i.e. is not None), and the token for the user and

    # email_confirmed status checks out
    if (email is not None and
            account_activation_token.check_token(email, token)):
        # Set user to active
        email.email_confirmed = True
        email.save()
        # Redirect to the desired page
        return render(request, 'activate.html')
    # If the user and/or token do not work, direct the user to an invalid page
    else:
        return render(request, 'account_activation_invalid.html')


class ViewEmail(TemplateView):

    template_name = "html_email_templates/standard_email.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            uidb64_value = kwargs['uidb64']
            uid = urlsafe_base64_decode(uidb64_value).decode()
            email_object = get_object_or_404(MassEmail, pk=uid)
        # If we can't get the email from the decoded primary key, raise 404

        except (TypeError, ValueError, OverflowError,
                EmailListEntry.DoesNotExist):
            raise Http404("Email does not exist.")
        if email_object is not None:
            pk = email_object.pk
            email_details = MassEmail.objects.get(pk=pk)
            print(email_details.subject)
            context["subject"] = email_details.subject
            context["message"] = email_details.message
            context["domain"] = settings.WEBSITE_URL
            context["email_uidb64"] = uid
            return context
        else:
            raise Http404("Email does not exist.")
