
from django.db import models
from django.db.models.signals import pre_delete, pre_save
from django.utils.translation import gettext_lazy as _
from django.contrib.sites.models import Site, _simple_domain_name_validator, SiteManager, SITE_CACHE, clear_site_cache

class SiteAliasManager(SiteManager):

    def _get_site_by_request(self, request):
        '''
        This version does an extra check for an alias fist to get the 
        '''
        host = request.get_host()
      
        try:                                                # First attempt to look up the site by the alias
            if host not in SITE_CACHE:
                alias = self.get(domain__iexact=host)
                SITE_CACHE[alias.domain] = alias.site
            return SITE_CACHE[host]
        except SiteAlias.DoesNotExist:
            try:
                SITE_CACHE[host] = Site.objects.get(domain__iexact=host)
                return SITE_CACHE[host]
            except Site.DoesNotExist:
                return Site.objects.get_current(request)
    
    def get_current(self, request=None):
        if request:
            return self._get_site_by_request(request)
        ## This will return the site from settings.SITE_ID
        return Site.objects.get_current()

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

def clear_all_aliases_cache(sender, **kwargs):
    site = kwargs['instance']
    SITE_CACHE = {}

def clear_alias_cache(sender, **kwargs):
    alias = kwargs['instance']
    try:
        del SITE_CACHE[alias.domain]
    except KeyError:
        pass
    clear_site_cache(sender=SiteAlias, instance=alias.site, using=None)

pre_save.connect(clear_alias_cache, sender=SiteAlias)
pre_delete.connect(clear_alias_cache, sender=SiteAlias)

pre_save.connect(clear_all_aliases_cache, sender=Site)
pre_delete.connect(clear_all_aliases_cache, sender=Site)