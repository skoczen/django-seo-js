from mock import Mock
from django.test import TestCase
from django.test.utils import override_settings
from httmock import all_requests, HTTMock, urlmatch

from django_seo_js.backends import PrerenderIO

MOCK_RESPONSE = "<html><body><h1>Hello, World!</h1></body></html>"
MOCK_RECACHE_RESPONSE = "OK"

@all_requests
def mock_prerender_recache_response(url, request):
    return { 
        'status_code': 200,
        'content': MOCK_RECACHE_RESPONSE,
    }

@all_requests
def mock_prerender_response(url, request):
    return { 
        'status_code': 200,
        'content': MOCK_RESPONSE,
    }


class PrerenderIOTestToken(TestCase):

    @override_settings(SEO_JS_PRERENDER_TOKEN=None)
    def test_get_token_throws_exception_if_missing(self):
        self.assertRaises(ValueError, PrerenderIO)

    @override_settings(SEO_JS_PRERENDER_TOKEN="123124341adfsaf")
    def test_get_token(self):
        self.backend = PrerenderIO()
        # Test function
        self.assertEqual(self.backend._get_token(), "123124341adfsaf")
        # Test __init__
        self.assertEqual(self.backend.token, "123124341adfsaf")


class PrerenderIOTestMethods(TestCase):

    def setUp(self):
        self.backend = PrerenderIO()

    def test_get_rendered_page_missing_url(self):
        self.assertRaises(TypeError, self.backend.get_rendered_page)
        self.assertRaises(ValueError, self.backend.get_rendered_page, None)

    def test_get_rendered_page_valid(self):
        with HTTMock(mock_prerender_response):
            self.assertEqual(MOCK_RESPONSE, self.backend.get_rendered_page("http://www.example.com"))

    def test_update_url_with_url_only(self):
        with HTTMock(mock_prerender_recache_response):
            resp = self.backend.update_url(url="http://www.example.com")
            self.assertEqual(resp, MOCK_RECACHE_RESPONSE)

    def test_update_url_with_regex_only(self):
        with HTTMock(mock_prerender_recache_response):
            resp = self.backend.update_url(regex="http://www.example.com/*")
            self.assertEqual(resp, MOCK_RECACHE_RESPONSE)

    def test_update_url_missing_url_and_regex(self):
        with HTTMock(mock_prerender_recache_response):
            self.assertRaises(ValueError, self.backend.update_url)
