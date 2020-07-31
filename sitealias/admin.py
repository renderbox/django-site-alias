from django.contrib import admin
from .models import SiteAlias


@admin.register(SiteAlias)
class SiteAliasAdmin(admin.ModelAdmin):
    list_display = ('domain', 'name', 'site')
    search_fields = ('domain', 'name', 'site')