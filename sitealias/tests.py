from sitealias.models import SiteAlias
from django.test import TestCase, Client, override_settings
from django.urls import reverse
from django.core.management import call_command
from django.contrib.sites.models import SITE_CACHE
from django.conf import settings
# Create your tests here.

TEST_HOSTS = settings.ALLOWED_HOSTS + ['alias-one.example-two.com', 'www.example-two.com']

class SystemTests(TestCase):
    
    def test_for_missing_migrations(self):
    
        result = call_command("makemigrations", check=True, dry_run=True)
        
        self.assertIsNone(result)

@override_settings(ALLOWED_HOSTS=TEST_HOSTS)
class MiddleWareTests(TestCase):
    
    fixtures = ["unit_test"]
    
    def setUp(self):
        self.client = Client()
        return super().setUp()

    def test_site_attaches_environment_SITE_ID_by_default(self):
        url = reverse('test_view')
        response = self.client.get(url)
        self.assertContains(response, 'Test Response')
        self.assertEqual(response.wsgi_request.site.id, 1)

    def test_allowed_alias_attaches_correct_site(self):
        response = self.client.get('/test/', HTTP_HOST='alias-one.example-two.com')
        self.assertContains(response, 'Test Response')
        self.assertEqual(response.wsgi_request.site.id, 2)
    
    def test_alias_not_allowed_reponds_with_400(self):
        response = self.client.get('/test/', HTTP_HOST='pretend-alias.example-two.com')
        self.assertContains(response, 'Bad Request', status_code=400)
        self.assertFalse(hasattr(response.wsgi_request, "site"))

@override_settings(ALLOWED_HOSTS=TEST_HOSTS)
class SiteCacheTest(TestCase):
    fixtures = ["unit_test"]
    
    def setUp(self):
        self.client = Client()

    def test_site_remove_from_SITE_CACHE_after_model_update(self):
        alias = SiteAlias.objects.get(pk=1)
        self.assertNotIn(alias, SITE_CACHE)
        response = self.client.get('/test/', HTTP_HOST='alias-one.example-two.com')
        self.assertContains(response, 'Test Response')
        self.assertEqual(response.wsgi_request.site.id, 2)
        self.assertIn(alias.domain, SITE_CACHE)

@override_settings(ALLOWED_HOSTS=TEST_HOSTS)
class SiteSignalTests(TestCase):
    
    fixtures = ["unit_test"]
    
    def setUp(self):
        self.client = Client()
        self.client.get('/test/', HTTP_HOST='alias-one.example-two.com')
        self.alias = SiteAlias.objects.get(pk=1)
        
        self.assertIn(self.alias.domain, SITE_CACHE)
        
        return super().setUp()

    def test_alias_removed_from_SITE_CACHE_after_model_update(self):

        self.alias.domain = 'alias-one-edit.example-two.com'
        self.alias.save()

        self.assertNotIn(self.alias.domain, SITE_CACHE)
    
    def test_alias_removed_from_SITE_CACHE_after_model_delete(self):

        self.alias.delete()

        self.assertNotIn(self.alias.domain, SITE_CACHE)
    
    def test_alias_and_parent_site_removed_from_SITE_CACHE_after_model_update(self):
        parent_site = self.alias.site.domain
        self.assertIn(self.alias.domain, SITE_CACHE)
        
        self.client.get('/test/', HTTP_HOST=parent_site)
        self.assertIn(parent_site, SITE_CACHE)
        
        self.alias.delete()

        self.assertNotIn(self.alias.domain, SITE_CACHE)
        self.assertNotIn(parent_site, SITE_CACHE)

