from django.urls import path

from sitealiases import views

urlpatterns = [
    path("", views.SiteAliasesIndexView.as_view(), name="sitealiases-index"),
]
