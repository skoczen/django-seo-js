from mock import Mock
from django.test import TestCase
from django.test.utils import override_settings


class BackendTest(TestCase):
    def test_update_the_render_cache(self):
        self.assertEqual("Tests written", True)
