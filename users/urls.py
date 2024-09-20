# users/urls.py
from django.urls import path
from . import views

from django.views.generic import TemplateView


# These are for the custom user views. We are still using some of django's
# built-in user views in django.contrib.auth.urls (like login
# and password_reset).
# The path to the custom URLs is listed in the pops_website/urls.py file.
urlpatterns = [
    path("signup/", views.sign_up, name="signup"),
    path(
        "account_activation_sent/",
        views.account_activation_sent,
        name="account_activation_sent",
    ),
    path("activate/<uidb64>/<token>/", views.activate, name="activate"),
    path("my_account/", views.my_account, name="my_account"),
    path("update/", views.UpdateAccount.as_view(), name="update_account"),
    path("email_list/subscribe/", views.AddNewEmail.as_view(), name="subscribe_email"),
    path("email_list/subscribe/error", views.AddNewEmailError.as_view(), name="subscribe_email_error"),
    path(
        "email_list/unsubscribe/<uidb64>/",
        views.DeleteEmail.as_view(),
        name="unsubscribe_email",
    ),
    path(
        "email_list/unsubscribe_successful/",
        TemplateView.as_view(template_name="accounts/unsubscribe_successful.html"),
        name="unsubscribe_successful",
    ),
    path("confirm_email/<uidb64>/<token>/", views.confirm_email, name="confirm_email"),
    path("email/<uidb64>/", views.ViewEmail.as_view(), name="view_email"),
]
