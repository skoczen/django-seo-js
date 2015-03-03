from django.test import TestCase

from django_seo_js.tests.utils import override_settings
from django_seo_js.middleware import EscapedFragmentMiddleware


class HelpersTest(TestCase):

    @override_settings(BACKEND='django_seo_js.backends.TestBackend')
    def test_update_the_render_cache(self):
        from django_seo_js.helpers import update_cache_for_url
        self.middleware = EscapedFragmentMiddleware()
        self.assertEqual(update_cache_for_url("http://example.com"), True)

    @override_settings(BACKEND='django_seo_js.backends.TestBackend', ENABLED=False)
    def test_update_skips_if_disabled(self):
        from django_seo_js.helpers import update_cache_for_url
        self.middleware = EscapedFragmentMiddleware()
        self.assertEqual(update_cache_for_url("http://example.com"), False)
