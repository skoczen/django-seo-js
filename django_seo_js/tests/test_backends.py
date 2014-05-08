from mock import Mock
from django.test import TestCase
from django.test.utils import override_settings

from django_seo_js.backends import PrerenderHosted, PrerenderIO, SelectedBackend, SEOBackendBase

class PrerenderHostedTest(TestCase):
    def test_not_done(self):
        self.assertEqual("Tests written", True)

class PrerenderIOTest(TestCase):
    def test_not_done(self):
        self.assertEqual("Tests written", True)

class SelectedBackendTest(TestCase):
    def test_not_done(self):
        self.assertEqual("Tests written", True)

class SEOBackendBaseTest(TestCase):
    def test_not_done(self):
        self.assertEqual("Tests written", True)
