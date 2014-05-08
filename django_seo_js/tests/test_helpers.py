from mock import Mock
from django.test import TestCase
from django.test.utils import override_settings

from django_seo_js.middleware import HashBangMiddleware

class HelpersTest(TestCase):

    @override_settings(SEO_JS_BACKEND='django_seo_js.backends.TestBackend')
    def test_update_the_render_cache(self):
        from django_seo_js.helpers import update_cache_for_url
        self.middleware = HashBangMiddleware()
        self.assertEqual(update_cache_for_url("http://example.com"), "Test worked")
        
