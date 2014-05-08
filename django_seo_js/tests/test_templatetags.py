from mock import Mock
from django.test import TestCase
from django.test.utils import override_settings


class TagsTest(TestCase):
    def test_not_done(self):
        self.assertEqual("Tests written", True)
