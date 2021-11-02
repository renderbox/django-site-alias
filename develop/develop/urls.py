"""develop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from sitealias.views import SiteAliasListView, my_view, SiteAliasUpdateView, SiteAliasDeleteView, SiteAliasCreateView
urlpatterns = [
    path(
            "",
            SiteAliasListView.as_view(),
            name="alias-list"
        ),
    path(
            "aliases/<int:pk>/update/",
            SiteAliasUpdateView.as_view(),
            name="alias-update"
        ),
     path(
            "aliases/<int:pk>/delete/",
            SiteAliasDeleteView.as_view(),
            name="alias-delete"
        ),
     path(
            "aliases/create/",
            SiteAliasCreateView.as_view(),
            name="alias-create"
        ),
    path('admin/', admin.site.urls),
]

if settings.TESTING:
    urlpatterns += [
        path('test/', my_view, name="test_view"),
    ]
