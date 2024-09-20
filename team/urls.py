# team/urls.py
from django.urls import path
from . import views
from django.views.generic import TemplateView, RedirectView
from django.conf import settings


urlpatterns = [
    path("team/", views.MemberListView.as_view(), name="team"),
]

""" if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) """
