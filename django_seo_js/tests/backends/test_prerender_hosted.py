from __future__ import unicode_literals

import random
import string

from django.test import TestCase
from httmock import all_requests, HTTMock

from django_seo_js.tests.utils import override_settings
from django_seo_js.backends import PrerenderHosted

MOCK_RESPONSE = b"<html><body><h1>Hello, World!</h1></body></html>"
MOCK_RESPONSE_HEADERS = {"foo": "bar"}
MOCK_RECACHE_RESPONSE = "OK"
MOCK_RECACHE_HEADERS = {"ibbity": "ack"}
_ascii = string.ascii_uppercase + string.digits
MOCK_GIANT_RESPONSE = ''.join(random.choice(_ascii) for _ in range(200000)).encode('ascii')


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


@all_requests
def mock_prerender_giant_response(url, request):
    return {
        'status_code': 200,
        'content': MOCK_GIANT_RESPONSE,
    }


class PrerenderHostedTestURLs(TestCase):

    @override_settings(PRERENDER_RECACHE_URL="http://example.com")
    def test_init_throws_exception_if_render_url_is_missing(self):
        self.assertRaises(ValueError, PrerenderHosted)

    @override_settings(PRERENDER_URL="http://example.com")
    def test_init_throws_exception_if_recache_url_is_missing(self):
        self.assertRaises(ValueError, PrerenderHosted)

    def test_init_throws_exception_if_both_urls_are_missing(self):
        self.assertRaises(ValueError, PrerenderHosted)

    @override_settings(
        PRERENDER_RECACHE_URL="http://example.com/recache",
        PRERENDER_URL="http://example.com"
    )
    def test_no_exception_if_both_are_provided(self):
        self.backend = PrerenderHosted()


class PrerenderHostedTestMethods(TestCase):

    @override_settings(
        PRERENDER_RECACHE_URL="http://example.com/recache",
        PRERENDER_URL="http://example.com"
    )
    def setUp(self):
        self.backend = PrerenderHosted()

    def test_get_response_for_url_missing_url(self):
        self.assertRaises(TypeError, self.backend.get_response_for_url)
        self.assertRaises(ValueError, self.backend.get_response_for_url, None)

    def test_get_response_for_url_valid(self):
        with HTTMock(mock_prerender_response):
            resp = self.backend.get_response_for_url("http://www.example.com")
            self.assertEqual(MOCK_RESPONSE, resp.content)
            for k, v in MOCK_RESPONSE_HEADERS.items():
                self.assertEqual(resp[k], v)

    def test_get_response_for_giant_response(self):
        with HTTMock(mock_prerender_giant_response):
            resp = self.backend.get_response_for_url("http://www.example.com")
            self.assertEqual(MOCK_GIANT_RESPONSE, resp.content)

    def test_update_url_with_url(self):
        with HTTMock(mock_prerender_recache_response):
            resp = self.backend.update_url(url="http://www.example.com")
            self.assertEqual(resp, True)

    def test_update_url_missing_url(self):
        with HTTMock(mock_prerender_recache_response):
            self.assertRaises(ValueError, self.backend.update_url)
