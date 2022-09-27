from django.test import TestCase

from django_seo_js.tests.utils import override_settings, get_response_empty
from django_seo_js.backends import PrerenderIO, SelectedBackend, SelectedBackendMixin, SEOBackendBase, TestBackend


class SEOBackendBaseTest(TestCase):
    def setUp(self):
        self.backend = SEOBackendBase()

    def test_get_response_for_url(self):
        self.assertRaises(NotImplementedError, self.backend.get_response_for_url, "http://www.example.com")

    def test_update_url(self):
        self.assertRaises(NotImplementedError, self.backend.update_url, "http://www.example.com")


class SelectedBackendTest(TestCase):

    def test_default_backend(self):
        s_mixin = SelectedBackendMixin()
        s = SelectedBackend(get_response_empty)
        self.assertTrue(isinstance(s_mixin.backend, PrerenderIO))
        self.assertTrue(isinstance(s.backend, PrerenderIO))

    @override_settings(BACKEND='django_seo_js.backends.TestBackend')
    def test_override_backend(self):
        s_mixin = SelectedBackendMixin()
        s = SelectedBackend(get_response_empty)
        self.assertTrue(isinstance(s_mixin.backend, TestBackend))
        self.assertTrue(isinstance(s.backend, TestBackend))
