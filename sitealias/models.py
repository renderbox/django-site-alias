
from django.db import models
from django.db.models.signals import pre_delete, pre_save
from django.utils.translation import gettext_lazy as _
from django.contrib.sites.models import Site, _simple_domain_name_validator, SiteManager, SITE_CACHE, clear_site_cache


# from django.core.exceptions import ImproperlyConfigured, ValidationError
from django.http.request import split_domain_port


class SiteAliasManager(SiteManager):

    def _get_site_by_request(self, request):
        '''
        This version does an extra check for an alias fist to get the 
        '''
        host = request.get_host()

        try:                                                # First attempt to look up the site by the alias
            if host not in SITE_CACHE:
                host = self.get(domain__iexact=host)
                SITE_CACHE[host] = host.site                # Use the Alias as the key and add the Alias's Site object to the cache
            return SITE_CACHE[host]
        except SiteAlias.DoesNotExist:
            return super()._get_site_by_request(request)


class SiteAlias(models.Model):
    '''
    This is meant to be a simple drop in replacement for the Django Site framework with the exception that it manages aliases
    '''

    domain = models.CharField(
        _('domain name'),
        max_length=100,
        validators=[_simple_domain_name_validator],
        unique=True,
    )
    name = models.CharField(_('display name'), max_length=50)
    site = models.ForeignKey(Site, verbose_name=_("Parent Site"), on_delete=models.CASCADE)

    objects = SiteAliasManager()

    class Meta:
        verbose_name = _('site alias')
        verbose_name_plural = _('site aliases')
        ordering = ['site', 'domain']

    def __str__(self):
        return self.domain

    def natural_key(self):
        return (self.domain,)

# TODO: Add feature to clear caches on all aliases when a Site is updated or deleted

pre_save.connect(clear_site_cache, sender=SiteAlias)
pre_delete.connect(clear_site_cache, sender=SiteAlias)
