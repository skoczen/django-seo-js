from django.test import TestCase
from django.test.utils import override_settings

from django_seo_js.backends import PrerenderIO, SelectedBackend, SEOBackendBase, TestBackend


class SEOBackendBaseTest(TestCase):
    def setUp(self):
        self.backend = SEOBackendBase()

    def test_get_response_for_url(self):
        self.assertRaises(NotImplementedError, self.backend.get_response_for_url, "http://www.example.com")

    def test_update_url(self):
        self.assertRaises(NotImplementedError, self.backend.update_url, "http://www.example.com")


class SelectedBackendTest(TestCase):

    def test_default_backend(self):
        s = SelectedBackend()
        self.assertTrue(isinstance(s.backend, PrerenderIO))

    @override_settings(SEO_JS_BACKEND='django_seo_js.backends.TestBackend')
    def test_override_backend(self):
        s = SelectedBackend()
        self.assertTrue(isinstance(s.backend, TestBackend))
