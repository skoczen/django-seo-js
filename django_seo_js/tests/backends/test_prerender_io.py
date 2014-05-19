from django.test import TestCase
from django.test.utils import override_settings
from httmock import all_requests, HTTMock

from django_seo_js.backends import PrerenderIO

MOCK_RESPONSE = "<html><body><h1>Hello, World!</h1></body></html>"
MOCK_RESPONSE_HEADERS = {"foo": "bar"}
MOCK_RECACHE_RESPONSE = "OK"
MOCK_RECACHE_HEADERS = {"ibbity": "ack"}


@all_requests
def mock_prerender_recache_response(url, request):
    return {
        'status_code': 200,
        'content': MOCK_RECACHE_RESPONSE,
        'headers': MOCK_RECACHE_HEADERS,
    }


@all_requests
def mock_prerender_response(url, request):
    return {
        'status_code': 200,
        'content': MOCK_RESPONSE,
        'headers': MOCK_RESPONSE_HEADERS,
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

    def test_get_response_for_url_missing_url(self):
        self.assertRaises(TypeError, self.backend.get_response_for_url)
        self.assertRaises(ValueError, self.backend.get_response_for_url, None)

    def test_get_response_for_url_valid(self):
        with HTTMock(mock_prerender_response):
            resp = self.backend.get_response_for_url("http://www.example.com")
            self.assertEqual(MOCK_RESPONSE, resp.content)
            for k, v in MOCK_RESPONSE_HEADERS.items():
                self.assertEqual(resp[k], v)

    def test_update_url_with_url_only(self):
        with HTTMock(mock_prerender_recache_response):
            resp = self.backend.update_url(url="http://www.example.com")
            self.assertEqual(resp, True)

    def test_update_url_with_regex_only(self):
        with HTTMock(mock_prerender_recache_response):
            resp = self.backend.update_url(regex="http://www.example.com/*")
            self.assertEqual(resp, True)

    def test_update_url_missing_url_and_regex(self):
        with HTTMock(mock_prerender_recache_response):
            self.assertRaises(ValueError, self.backend.update_url)
