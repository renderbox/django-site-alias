from django.test import TestCase, Client, override_settings
from django.urls import reverse
from django.views.defaults import bad_request
from django.conf import settings
# Create your tests here.

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

    @override_settings(ALLOWED_HOSTS=['alias-one.example-two.com', 'www.example-two.com'])
    def test_allowed_alias_attaches_correct_site(self):
        response = self.client.get('/test/', HTTP_HOST='alias-one.example-two.com')
        self.assertContains(response, 'Test Response')
        self.assertEqual(response.wsgi_request.site.id, 2)
    
    @override_settings(ALLOWED_HOSTS=['alias-one.example-two.com', 'www.example-two.com'])
    def test_alias_not_allowed_reponds_with_400(self):
        response = self.client.get('/test/', HTTP_HOST='pretend-alias.example-two.com')
        self.assertContains(response, 'Bad Request', status_code=400)
        self.assertFalse(hasattr(response.wsgi_request, "site"))