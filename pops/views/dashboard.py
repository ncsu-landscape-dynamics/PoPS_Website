from django.views.generic import (
    FormView,
    ListView,
    DetailView,
    TemplateView,
    CreateView,
    UpdateView,
    View,
    DeleteView,
)
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import UserPassesTestMixin
import json
from django.http import (
    JsonResponse,
    HttpResponse,
    HttpResponseForbidden,
    HttpResponseRedirect,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import ensure_csrf_cookie

from django.db.models.functions import Greatest
from django.db.models import (
    Prefetch,
    Sum,
    Count,
    Exists,
    Max,
    Min,
    OuterRef,
    Subquery,
    Q,
)

from ..models import *
from ..forms import *

from users.models import CustomUser

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

def temp_view(request):
    return render(request, "pops/dashboard/temp.html")


class SessionAjaxableResponseMixin:
    """
    Mixin to add AJAX support to a form.
    Must be used with an object-based FormView (e.g. CreateView)
    """

    def form_invalid(self, form):
        response = super().form_invalid(form)
        if self.request.accepts("application/json"):
            return JsonResponse(form.errors, status=400)
        else:
            return response

    def form_valid(self, form):
        # We make sure to call the parent's form_valid() method because
        # it might do some processing (in the case of CreateView, it will
        # call form.save() for example).
        form.instance.created_by = self.request.user
        response = super().form_valid(form)
        session_id = self.object.pk
        new_run_collection = RunCollection(
            session=self.object, name="Default", default=True
        )
        new_run_collection.save()
        new_run = Run(run_collection=new_run_collection)
        new_run.save()
        session = self.object
        session.default_run = new_run
        session.save()
        if self.request.accepts("application/json"):
            data = {
                "session_pk": self.object.pk,
                "run_collection_pk": new_run_collection.pk,
                "run_pk": new_run.pk,
                "case_study_pk": self.object.case_study.pk,
            }
            return JsonResponse(data)
        else:
            return response


class NewSessionView(LoginRequiredMixin, SessionAjaxableResponseMixin, CreateView):
    template_name = "pops/dashboard/new_session.html"
    form_class = SessionForm
    login_url = "login"

    def get_initial(self, *args, **kwargs):
        initial = super(NewSessionView, self).get_initial(**kwargs)
        try:
            case_study = self.kwargs.get("case_study")
        except:
            case_study = None
        initial["case_study"] = case_study
        return initial

    def get_context_data(self, **kwargs):
        context = super(NewSessionView, self).get_context_data(**kwargs)

        if self.request.accepts("application/json"):
            return context
        else:
            case_study = self.kwargs.get("case_study")
            print(case_study)
            

            if case_study:
                print('Case study is true')
            else:
                print('Case study is none')

            # Here we are grabbing the first pest associated with a case study
            # This needs to be changed if we start handling case studies with multiple pests
            pest = Pest.objects.filter(case_study__pk=case_study)[:1].get()
            print(pest)
            #reproductive_rate = ReproductiveRate.objects.filter(pest=pest)
            #distance_scale = PlottingDistanceScale.objects.get(parameters=pest.parameters)
            """ context["form"].fields["case_study"].queryset = CaseStudy.objects.filter(
                pk=case_study
            ) """
            #print(distance_scale)
            #print(len(distance_scale.values))
            #print(distance_scale.values[1])
            #values=[]
            #for val in distance_scale.values:
            #    print(val)
            #    values.append(val)
            #print(values)
            #print(distance_scale.probabilities[1])
            #print(distance_scale.minimum)
            case_study = CaseStudy.objects.get(pk=case_study)
            context["case_study"] = case_study

            """ context["pest"] = (
                Pest.objects.select_related("vector")
                .filter(case_study__pk=case_study)
                .select_related("pest_information")
            )
            context["reproductive_rates"] = reproductive_rate.order_by("value")
            context["min_reproductive_rate"] = reproductive_rate.order_by(
                "value"
            ).first()
            context["max_reproductive_rate"] = reproductive_rate.order_by(
                "value"
            ).last()
            context["expected_reproductive_rate"] = reproductive_rate.order_by(
                "-probability"
            ).first()
            context["distances"] = natural_distance.order_by("value")
            context["min_distance"] = natural_distance.order_by("value").first()
            context["max_distance"] = natural_distance.order_by("-value").first()
            context["expected_distance"] = natural_distance.order_by(
                "-probability"
            ).first() """
            #context["distance_scale"]=distance_scale
            return context

    def get_success_url(self, **kwargs):
        # obj = form.instance or self.object
        return reverse("dashboard", kwargs={"pk": self.object.pk})


""" class NewSessionView(CreateView):
    template_name = 'pops/dashboard/new_session.html'
    form_class = SessionForm

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        form.instance.created_by = self.request.user
        return super().form_valid(form)

    def get_success_url(self, **kwargs):
        # obj = form.instance or self.object
        return reverse("dashboard", kwargs={'pk': self.object.pk})
 """


class WorkspaceView(LoginRequiredMixin, TemplateView):
    template_name = "pops/dashboard/workspace.html"
    login_url = "login"

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(WorkspaceView, self).get_context_data(**kwargs)
        current_user = self.request.user
        context["current_user"] = current_user
        context["user_case_studies"] = (
            CaseStudy.objects.prefetch_related("pest_set__pest_information")
            .filter(created_by=current_user)
            .order_by("-date_created")[:5]
        )
        # context['user_sessions'] = Session.objects.annotate(number_runs=Count('runcollection')).annotate(most_recent_run=Max('runcollection__date_created')).prefetch_related('created_by','case_study').filter(created_by = self.request.user).order_by('-date_created')[:5]
        context["sessions"] = (
            Session.objects.prefetch_related("created_by", "case_study")
            .filter(Q(created_by=current_user) | Q(allowedusers__user=current_user))
            .filter(default_run__status="SUCCESS")
            .annotate(shared=Count("allowedusers", distinct=True))
            .annotate(number_runs=Count("runcollection", distinct=True))
            .annotate(most_recent_run=Max("runcollection__date_created"))
            .order_by("-most_recent_run")[:5]
        )
        context["number_of_sessions"] = Session.objects.filter(
            Q(created_by=current_user) | Q(allowedusers__user=current_user)
        ).count()
        context["number_of_case_studies"] = CaseStudy.objects.filter(
            created_by=current_user
        ).count()
        return context


class SessionListView(LoginRequiredMixin, TemplateView):
    login_url = "login"
    # paginate_by = 5  # if pagination is desired
    template_name = "pops/dashboard/session_list.html"

    def get_queryset(self):
        return (
            Session.objects.annotate(number_runs=Count("runcollection"))
            .annotate(most_recent_run=Max("runcollection__date_created"))
            .prefetch_related("created_by", "case_study")
            .filter(created_by=self.request.user)
            .order_by("-date_created")
        )

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(SessionListView, self).get_context_data(**kwargs)
        current_user = self.request.user
        context["sessions"] = (
            Session.objects.prefetch_related("created_by", "case_study")
            .filter(Q(created_by=current_user) | Q(allowedusers__user=current_user))
            .filter(default_run__status="SUCCESS")
            .annotate(shared=Count("allowedusers", distinct=True))
            .annotate(number_runs=Count("runcollection", distinct=True))
            .annotate(most_recent_run=Max("runcollection__date_created"))
            .order_by("-most_recent_run")
        )
        return context


class SessionShareView(LoginRequiredMixin, CreateView):
    login_url = "login"
    template_name = "pops/dashboard/session_share.html"
    model = AllowedUsers
    fields = ["session", "user"]

    def get_success_url(self, **kwargs):
        return reverse("session_share", kwargs={"pk": self.object.session.pk})

    def get(self, request, *args, **kwargs):
        pk = self.kwargs.get("pk")
        if pk:
            permission = self.check_permissions(request, pk=pk)
            if not permission:
                return HttpResponseForbidden()
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        pk = self.kwargs.get("pk")
        if pk:
            permission = self.check_permissions(request, pk=pk)
            if not permission:
                return HttpResponseForbidden()
        if "user" in request.POST:
            return super().post(request, *args, **kwargs)
        elif "public" in request.POST:
            data = request.POST.copy()
            obj = Session.objects.get(pk=pk)
            obj.public = data.get("public")
            obj.save()
            return HttpResponseRedirect(reverse("session_share", kwargs={"pk": pk}))
        else:
            return HttpResponseRedirect(reverse("session_share", kwargs={"pk": pk}))

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(SessionShareView, self).get_context_data(**kwargs)
        pk = self.kwargs.get("pk")
        try:
            session = Session.objects.get(pk=pk)
        except:
            session = None
        users = CustomUser.objects.filter(is_active=True)
        allowed_users = AllowedUsers.objects.filter(session=self.kwargs.get("pk"))
        context["allowed_users"] = allowed_users
        # context['users'] = users
        context["session"] = session
        return context

    def check_permissions(self, request, pk):
        session = get_object_or_404(Session, pk=pk)
        if session.created_by == request.user:
            return True
        return


# Send a list of PoPS users that meet the search criteria on the session share page
def get_users(request):
    user_search = request.GET.get("q")  # string entered by the user
    splitquery = user_search.split()  # split the query into individual words
    session = request.GET.get("session")  # get session
    q_objects = Q()  # init our q objects variable to use .add() on it
    # create a complex Q object to query for the users based on any
    # matches to first name, last name or username
    for words in splitquery:
        search_fields = ["first_name", "last_name", "username"]
        for term in splitquery:
            for field_name in search_fields:
                q_objects.add(Q(**{"%s__icontains" % field_name: term}), Q.OR)
    # create object list of user matches, excluding users already in this shared session
    user_matches = CustomUser.objects.exclude(
        allowedusers__in=AllowedUsers.objects.filter(session=session)
    ).filter(q_objects)
    # create a list to send via json response
    data = {
        "users": list(
            user_matches.order_by("last_name").values(
                "pk", "first_name", "last_name", "username", "organization"
            )
        ),
    }
    return JsonResponse(data)


class DeleteAllowedUserView(LoginRequiredMixin, DeleteView):
    model = AllowedUsers

    def get_success_url(self, **kwargs):
        return reverse("session_share", kwargs={"pk": self.object.session.pk})

    def get(self, request, *args, **kwargs):
        pk = self.kwargs.get("pk")
        if pk:
            permission = self.check_permissions(request, pk=pk)
            if not permission:
                return HttpResponseForbidden()
        return self.post(request, *args, **kwargs)

    def check_permissions(self, request, pk):
        self.object = self.get_object()
        session = get_object_or_404(Session, pk=self.object.session.pk)
        if session.created_by == request.user:
            return True


class DeleteSessionView(LoginRequiredMixin, DeleteView):
    model = Session
    success_url = reverse_lazy("session_list")

    def get_queryset(self):
        owner = self.request.user
        return self.model.objects.filter(created_by=owner)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.created_by == request.user:
            success_url = self.get_success_url()
            self.object.delete()
            return HttpResponseRedirect(success_url)
        else:
            raise PermissionDenied


class DashboardTempView(TemplateView):
    template_name = "pops/dashboard/dashboard.html"

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(DashboardView, self).get_context_data(**kwargs)
        try:
            session = Session.objects.get(pk=self.kwargs.get("pk"))
        except:
            session = None
        context["session"] = session
        return context


class AjaxableResponseMixin:
    """
    Mixin to add AJAX support to a form.
    Must be used with an object-based FormView (e.g. CreateView)
    """

    def form_invalid(self, form):
        response = super().form_invalid(form)
        if self.request.accepts("application/json"):
            return JsonResponse(form.errors, status=400)
        else:
            return response

    def form_valid(self, form):
        # We make sure to call the parent's form_valid() method because
        # it might do some processing (in the case of CreateView, it will
        # call form.save() for example).
        response = super().form_valid(form)
        if self.request.accepts("application/json"):
            data = {
                "pk": self.object.pk,
                "name": self.object.name,
                "description": self.object.description,
                "date": self.object.date_created,
            }
            s1 = json.dumps(data, indent=4, sort_keys=True, default=str)
            l1 = json.loads(s1)
            layer = get_channel_layer()
            session_group_id = 'chat_%s' % 2 #self.session_id
            async_to_sync(layer.group_send)(session_group_id, {
                'type': 'events.alarm',
                'content': s1
            })
            return JsonResponse(data)
        else:
            return response


class DashboardView(AjaxableResponseMixin, LoginRequiredMixin, CreateView):
    template_name = "pops/dashboard/dashboard.html"
    form_class = RunCollectionForm
    success_url = "new_session"
    login_url = "login"

    def get(self, request, *args, **kwargs):
        pk = self.kwargs.get("pk")
        if pk:
            permission = self.check_permissions(request, pk=pk)
            if not permission:
                return HttpResponseForbidden()
        return super().get(request, *args, **kwargs)

    def check_permissions(self, request, pk):
        session = get_object_or_404(Session, pk=pk)

        return (
            session.created_by == request.user
            or session.public
            or session.allowedusers_set.filter(user=request.user).exists()
            )
        # if session.created_by == request.user:
        #     return True
        # elif session.public:
        #     return True
        # elif session.allowedusers_set.filter(user=request.user).exists():
        #     return True
        # return

    def get_initial(self):
        # call super if needed
        return {"session": self.kwargs.get("pk")}

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(DashboardView, self).get_context_data(**kwargs)
        try:
            session = Session.objects.get(pk=self.kwargs.get("pk"))
        except:
            session = None
            print("No session found")
        # Get case study pk
        allowed_users = AllowedUsers.objects.filter(session=session)
        case_study = session.case_study

        try:
            last_output = Output.objects.filter(
                run__run_collection=OuterRef("pk")
            ).order_by("-year")[:1]
            run_collections = (
                RunCollection.objects.annotate(overall_cost=Sum("run__management_cost"))
                .annotate(
                    infected_area=Subquery(last_output.values("infected_area")[:1])
                )
                .annotate(
                    number_infected=Subquery(last_output.values("number_infected")[:1])
                )
                .filter(session__pk=self.kwargs.get("pk"), default=False)
                .order_by("date_created")
            )  # .prefetch_related(Prefetch('output_set', queryset=Output.objects.defer('spread_map').order_by('years')))
        except:
            run_collections = None
            print("No run_collections found")

        for run_collection in run_collections:
            if run_collection.overall_cost == None:
                run_collection.overall_cost = 0
            if run_collection.infected_area == None:
                run_collection.infected_area = 0
            if run_collection.number_infected == None:
                run_collection.number_infected = 0

        try:
            historic_data = HistoricData.objects.filter(case_study=case_study).order_by(
                "year"
            )
        except:
            historic_data = None
            print("No historic data found")
        try:
            mapbox_parameters = MapBoxParameters.objects.get(case_study=case_study)
        except:
            mapbox_parameters = None
        try:
            host_maps = ClippedHostLocation.objects.filter(pest_host_interaction__pest__case_study=case_study)
            # This is grabbing the first host map. If there are multiple, due to multiple pests, we need to rethink
            # this line.
            host_map = host_maps[0].json_map 
        except:
            host = None
            host_map = None
            print("No host map found")
        try:
            pesticidelinks = PestPesticideLink.objects.filter(
                pest_information__pest__case_study=case_study
                ).prefetch_related('pesticide')
        except:
            pesticidelinks = None
            print("No pesticides in this case study")
        steering_years =  range(
            int(case_study.first_forecast_date.strftime('%Y')),
            int(case_study.last_forecast_date.strftime('%Y'))+1
            ) #Update range dynamically range(case_study.end_year + 1, session.final_year + 1)
        context["session"] = session
        context["case_study"] = case_study
        context["mapbox_parameters"] = mapbox_parameters
        context["historic_data"] = historic_data
        context["steering_years"] = steering_years
        context["run_collections"] = run_collections
        context["host_map"] = host_map
        context["allowed_users"] = allowed_users
        context["allowed_users_count"] = allowed_users.count()
        context["pesticidelinks"] = pesticidelinks
        return context


class WebsocketDashboardView(DashboardView):

    def get_context_data(self, **kwargs):
        context = super(WebsocketDashboardView, self).get_context_data(**kwargs)
        return context

@method_decorator(csrf_exempt, name="post")
class NewRunView(CreateView):
    template_name = "pops/dashboard/dashboard.html"
    form_class = RunForm
    success_url = "new_session"

    def post(self, request, *args, **kwargs):
        run_form = self.form_class(request.POST)
        if run_form.is_valid():
            new_run = run_form.save()
            if self.request.accepts("application/json"):
                data = {
                    "pk": new_run.pk,
                    "steering_year": new_run.steering_year,
                }
                return JsonResponse(data)
            else:
                return self.render_to_response(self.get_context_data(success=True))
        else:
            if self.request.accepts("application/json"):
                return JsonResponse(run_form.errors, status=400)
            else:
                return self.render_to_response(self.get_context_data(success=False))


@method_decorator(ensure_csrf_cookie, name="get")
class DashboardTestView(AjaxableResponseMixin, CreateView):
    template_name = "pops/dashboard/dashboard_test.html"
    form_class = RunCollectionForm
    success_url = "new_session"

    def get_initial(self):
        # call super if needed
        return {"session": self.kwargs.get("pk")}

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(DashboardTestView, self).get_context_data(**kwargs)
        try:
            session = Session.objects.get(pk=self.kwargs.get("pk"))
        except:
            session = None
        # Get case study pk
        case_study = session.case_study

        try:
            last_output = Output.objects.filter(
                run__run_collection=OuterRef("pk")
            ).order_by("-year")[:1]
            run_collections = (
                RunCollection.objects.annotate(overall_cost=Sum("run__management_cost"))
                .annotate(
                    infected_area=Subquery(last_output.values("infected_area")[:1])
                )
                .annotate(
                    number_infected=Subquery(last_output.values("number_infected")[:1])
                )
                .filter(session__pk=self.kwargs.get("pk"), default=False)
                .order_by("date_created")
            )  # .prefetch_related(Prefetch('output_set', queryset=Output.objects.defer('spread_map').order_by('years')))
        except:
            run_collections = None

        for run_collection in run_collections:
            if run_collection.overall_cost == None:
                run_collection.overall_cost = 0
            if run_collection.infected_area == None:
                run_collection.infected_area = 0
            if run_collection.number_infected == None:
                run_collection.number_infected = 0

        try:
            historic_data = HistoricData.objects.filter(case_study=case_study).order_by(
                "year"
            )
        except:
            historic_data = None
        try:
            mapbox_parameters = MapBoxParameters.objects.get(case_study=case_study)
        except:
            historic_data = None

        # try:
        # host = HostData.objects.filter(host__case_study=case_study).values('host_map').first()
        # host_map = host['host_map']
        # except:
        # host = None
        # host_map = None

        steering_years = range(case_study.end_year + 1, session.final_year + 1)
        context["session"] = session
        context["case_study"] = case_study
        context["mapbox_parameters"] = mapbox_parameters
        context["historic_data"] = historic_data
        context["steering_years"] = steering_years
        context["run_collections"] = run_collections
        # context['host_map'] = host_map
        return context


def get_run_collection(request):
    print("GETTING RUN COLLECTION:")
    run_collection_id = request.GET.get("run_collection_id", None)
    run_collection = RunCollection.objects.get(pk=run_collection_id)
    inputs = Run.objects.filter(run_collection=run_collection)
    data = {
        "pk": run_collection.pk,
        "name": run_collection.name,
        "description": run_collection.description,
        "status": run_collection.status,
        "random_seed": run_collection.random_seed,
        "date_created": run_collection.date_created,
        "budget": run_collection.budget,
        "tangible_landscape": run_collection.tangible_landscape,
        "inputs": list(
            inputs.order_by("steering_year").values(
                "pk", "date_created", "id", "steering_year"
            )
        ),
    }
    return JsonResponse(data)


def get_output_view(request):
    run_id = request.GET.get("new_run_id", None)
    this_run = Run.objects.get(pk=run_id)
    first_year = int(this_run.run_collection.session.case_study.first_forecast_date.strftime('%Y'))
    run_collection = this_run.run_collection
    total_management_cost = Run.objects.filter(run_collection=run_collection).aggregate(
        Sum("management_cost")
    )
    number_of_steering_runs = Run.objects.filter(run_collection=run_collection).count()
    steering_year = this_run.steering_year
    default_run = run_collection.session.default_run
    default_run_outputs = Output.objects.filter(run_id=default_run)
    spread_rate = default_run_outputs.annotate(
        max_spread=Greatest(
            "spreadrate__west_rate",
            "spreadrate__north_rate",
            "spreadrate__south_rate",
            "spreadrate__east_rate",
        )
    )
    max_spreadrate = spread_rate.aggregate(Max("max_spread"))
    maximum_spread_rate = max_spreadrate["max_spread__max"]
    defaults = {
        "steering_year": 0,
        "management_cost": 0,
        "management_area": 0,
        "output": list(
            default_run_outputs.order_by("year").values(
                "pk",
                "date_created",
                "id",
                "number_infected",
                "infected_area",
                "year",
                "escape_probability",
            )
        ),
    }
    # steering_outputs contains the information needed to make the side plots on the dashboard
    steering_outputs = []
    if steering_year:
        for x in range(first_year, first_year + number_of_steering_runs):
            run = Run.objects.get(run_collection=run_collection, steering_year=x)
            run_outputs = Output.objects.filter(run_id=run)
            steering_year_output = {
                "steering_year": run.steering_year,
                "management_cost": run.management_cost,
                "management_area": run.management_area,
                "output": list(
                    run_outputs.order_by("year").values(
                        "pk",
                        "date_created",
                        "id",
                        "number_infected",
                        "infected_area",
                        "year",
                        "escape_probability",
                    )
                ),
            }
            steering_outputs.append(steering_year_output)

        all_outputs = Output.objects.filter(run__run_collection=run_collection)
        spread_rate = all_outputs.annotate(
            max_spread=Greatest(
                "spreadrate__west_rate",
                "spreadrate__north_rate",
                "spreadrate__south_rate",
                "spreadrate__east_rate",
            )
        )
        max_steering_spreadrate = spread_rate.aggregate(Max("max_spread"))
        maximum_spread_rate = max(
            maximum_spread_rate, max_steering_spreadrate["max_spread__max"]
        )
    else:
        print("Steering year false")

    # get all inputs for runs in this collection (management polygons)
    inputs = Run.objects.filter(run_collection=run_collection)
    # get the outputs for this run (used for displaying on the map)
    outputs = Output.objects.filter(run_id=run_id)
    # then merge the outputs for previous runs to get the previous steering years
    if steering_year:
        steering_boolean = True
        for x in range(first_year, steering_year):
            run = Run.objects.get(run_collection=run_collection, steering_year=x)
            outputs = outputs | Output.objects.filter(run_id=run, year=x)
    else:
        steering_boolean = False
    data = {
        "run_inputs": {
            "primary_key": this_run.pk,
            "date_created": this_run.date_created,
            "status": this_run.status,
            "steering_year": this_run.steering_year,
            "management_cost": this_run.management_cost,
            "management_area": this_run.management_area,
            "management_polygons": this_run.management_polygons,
        },
        "inputs": list(
            inputs.order_by("steering_year").values(
                "pk",
                "date_created",
                "id",
                "steering_year",
                "management_cost",
                "management_polygons",
                "management_area",
            )
        ),
        "results": list(
            outputs.order_by("year").values(
                "pk",
                "date_created",
                "id",
                "number_infected",
                "infected_area",
                "year",
                "min_spread_map",
                "median_spread_map",
                "max_spread_map",
                "mean_spread_map",
                "standard_deviation_map",
                "probability_map",
                "escape_probability",
            )
        ),
        "spread_rate": list(
            outputs.order_by("year").values(
                "year",
                "spreadrate__west_rate",
                "spreadrate__north_rate",
                "spreadrate__south_rate",
                "spreadrate__east_rate",
            )
        ),
        "all_steering_years": steering_outputs,
        "no_management_default": defaults,
        "steering": steering_boolean,
        "max_spread_rate": maximum_spread_rate,
        "total_management_cost": total_management_cost["management_cost__sum"],
    }
    return JsonResponse(data)


def check_status(request):
    run_id = request.GET.get("new_run_id", None)
    run = Run.objects.get(pk=run_id)
    data = {
        "status": run.status,
    }
    return JsonResponse(data)


def check_for_new_TL_run(request):
    run_collection_id = request.GET.get("run_collection_id", None)
    print("Run collection id: " + run_collection_id)
    run_collection = RunCollection.objects.get(pk=run_collection_id)
    most_recent_run = (
        Run.objects.filter(run_collection=run_collection, status="SUCCESS")
        .order_by("pk")
        .last()
    )
    if most_recent_run is not None:
        print(most_recent_run)
        data = {
            "most_recent_run_pk": most_recent_run.pk,
            "steering_year": most_recent_run.steering_year,
        }
    else:
        data = {"most_recent_run_pk": 0}
    return JsonResponse(data)


def delete_runs(request):
    run_id = request.GET.get("run_id", None)
    run_collection = request.GET.get("run_collection", None)
    runs = Run.objects.filter(run_collection=run_collection, pk__gte=run_id)
    print("Run collection is:" + run_collection)
    print("The run id is:" + run_id)
    print(runs)
    runs.delete()
    data = {
        "run_id": run_id,
    }
    return JsonResponse(data)


def delete_run_collection(request):
    run_collection_id = request.GET.get("run_collection", None)
    run_collection = RunCollection.objects.get(pk=run_collection_id)
    print("Run collection is:" + run_collection_id)
    run_collection.delete()
    data = {
        "run_collection_id": run_collection_id,
    }
    return JsonResponse(data)


def edit_run_collection(request):
    run_collection_id = request.GET.get("run_collection", None)
    run_collection_name = request.GET.get("name", None)
    run_collectiond_description = request.GET.get("description", None)
    run_collection = RunCollection.objects.get(pk=run_collection_id)
    print("Run collection is:" + run_collection_id)
    run_collection.name = run_collection_name
    run_collection.description = run_collectiond_description
    run_collection.save()
    data = {
        "run_collection_id": run_collection_id,
    }
    return JsonResponse(data)


class OutputDetailView(LoginRequiredMixin, DetailView):
    template_name = "pops/dashboard/detail_output.html"
    model = Output

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
