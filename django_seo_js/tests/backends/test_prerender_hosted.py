from mock import Mock
from django.test import TestCase
from django.test.utils import override_settings
from httmock import all_requests, HTTMock, urlmatch

from django_seo_js.backends import PrerenderHosted

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


class PrerenderHostedTestURLs(TestCase):

    @override_settings(SEO_JS_PRERENDER_RECACHE_URL="http://example.com")
    def test_init_throws_exception_if_render_url_is_missing(self):
        self.assertRaises(ValueError, PrerenderHosted)

    @override_settings(SEO_JS_PRERENDER_URL="http://example.com")
    def test_init_throws_exception_if_recache_url_is_missing(self):
        self.assertRaises(ValueError, PrerenderHosted)

    def test_init_throws_exception_if_both_urls_are_missing(self):
        self.assertRaises(ValueError, PrerenderHosted)

    @override_settings(SEO_JS_PRERENDER_RECACHE_URL="http://example.com/recache", SEO_JS_PRERENDER_URL="http://example.com")
    def test_no_exception_if_both_are_provided(self):
        self.backend = PrerenderHosted()


class PrerenderHostedTestMethods(TestCase):

    @override_settings(SEO_JS_PRERENDER_RECACHE_URL="http://example.com/recache", SEO_JS_PRERENDER_URL="http://example.com")
    def setUp(self):
        self.backend = PrerenderHosted()

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
