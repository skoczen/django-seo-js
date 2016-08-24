from __future__ import unicode_literals

from mock import Mock
from django.test import TestCase

from django_seo_js.tests.utils import override_settings
from django_seo_js.middleware import EscapedFragmentMiddleware, UserAgentMiddleware, HashBangMiddleware

print(override_settings)


class BaseMiddlewareTest(TestCase):
    pass


class EscapedFragmentMiddlewareTest(TestCase):

    @override_settings(BACKEND='django_seo_js.backends.TestBackend')
    def setUp(self):
        super(EscapedFragmentMiddlewareTest, self).setUp()
        self.middleware = EscapedFragmentMiddleware()
        self.request = Mock()
        self.request.path = "/"
        self.request.GET = {}

    def test_has_escaped_fragment(self):
        self.request.GET = {"_escaped_fragment_": None}
        self.assertEqual(self.middleware.process_request(self.request).content, b"Test")

    def test_does_not_have_escaped_fragment(self):
        self.request.GET = {}
        self.assertEqual(self.middleware.process_request(self.request), None)

    @override_settings(BACKEND='django_seo_js.backends.TestBackend', ENABLED=False)
    def test_has_escaped_fragment_skips_if_disabled_via_enabled(self):
        self.middleware = EscapedFragmentMiddleware()
        self.request.GET = {}
        self.assertEqual(self.middleware.process_request(self.request), None)

    @override_settings(BACKEND='django_seo_js.backends.TestServiceDownBackend')
    def test_has_escaped_fragment_skips_if_service_is_down(self):
        self.middleware = EscapedFragmentMiddleware()
        self.request.GET = {"_escaped_fragment_": None}
        self.assertEqual(self.middleware.process_request(self.request), None)

    @override_settings(BACKEND='django_seo_js.backends.TestBackend')
    def test_overriding_skips_sitemap_xml_by_default(self):
        self.middleware = EscapedFragmentMiddleware()
        self.request.path = "/sitemap.xml"
        self.request.GET = {"_escaped_fragment_": None}
        self.assertEqual(self.middleware.process_request(self.request), None)

    @override_settings(
        BACKEND='django_seo_js.backends.TestBackend',
        IGNORE_URLS=["/foo.html", "/bar/ibbity.html", ],
        IGNORE_EXTENSIONS=[],
    )
    def test_overriding_skips_custom_overrides_xml_by_default(self):
        self.middleware = EscapedFragmentMiddleware()
        self.request.path = "/sitemap.xml"
        self.request.GET = {"_escaped_fragment_": None}
        self.assertEqual(self.middleware.process_request(self.request).content, b"Test")

        self.request.path = "/foo.html"
        self.assertEqual(self.middleware.process_request(self.request), None)

        self.request.path = "/bar/ibbity.html"
        self.assertEqual(self.middleware.process_request(self.request), None)

    @override_settings(BACKEND='django_seo_js.backends.TestBackend')
    def test_overriding_skips_gifs_by_default(self):
        self.middleware = EscapedFragmentMiddleware()
        self.request.path = "/sitemap.xml"
        self.request.GET = {"_escaped_fragment_": None}
        self.assertEqual(self.middleware.process_request(self.request), None)

    @override_settings(
        BACKEND='django_seo_js.backends.TestBackend',
        IGNORE_EXTENSIONS=[".html", ".txt", ]
    )
    def test_overriding_skips_custom_overrides_gifs_by_default(self):
        self.middleware = EscapedFragmentMiddleware()
        self.request.path = "/foo.gif"
        self.request.GET = {"_escaped_fragment_": None}
        self.assertEqual(self.middleware.process_request(self.request).content, b"Test")

        self.request.path = "/foo.html"
        self.assertEqual(self.middleware.process_request(self.request), None)

        self.request.path = "/bar/ibbity.txt"
        self.assertEqual(self.middleware.process_request(self.request), None)


class HashBangMiddlewareTest(EscapedFragmentMiddlewareTest):

    @override_settings(BACKEND='django_seo_js.backends.TestBackend')
    def setUp(self):
        super(HashBangMiddlewareTest, self).setUp()
        self.middleware = HashBangMiddleware()
        self.request = Mock()
        self.request.path = "/"
        self.request.GET = {}


class UserAgentMiddlewareTest(TestCase):

    @override_settings(BACKEND='django_seo_js.backends.TestBackend')
    def setUp(self):
        super(UserAgentMiddlewareTest, self).setUp()
        self.middleware = UserAgentMiddleware()
        self.request = Mock()
        self.request.path = "/"
        self.request.META = {}

    def test_matches_one_of_the_default_user_agents(self):
        self.request.META = {
            "HTTP_USER_AGENT":
            "Mozilla/2.0 (compatible; Ask Jeeves/Teoma; +http://about.ask.com/en/docs/about/webmasters.shtml)"
        }
        self.assertEqual(self.middleware.process_request(self.request).content, b"Test")

    def test_does_not_match_one_of_the_default_user_agents(self):
        self.request.META = {
            "HTTP_USER_AGENT": "This user-agent is not a search engine."
        }
        self.assertEqual(self.middleware.process_request(self.request), None)

    @override_settings(
        USER_AGENTS=["TestUserAgent", ],
        BACKEND='django_seo_js.backends.TestBackend'
    )
    def test_overriding_matches(self):
        self.middleware = UserAgentMiddleware()
        self.request.META = {
            "HTTP_USER_AGENT": "The TestUserAgent v1.0"
        }
        self.assertEqual(self.middleware.process_request(self.request).content, b"Test")

    @override_settings(
        USER_AGENTS=["TestUserAgent", ],
        BACKEND='django_seo_js.backends.TestBackend'
    )
    def test_overriding_does_not_match_properly(self):
        self.middleware = UserAgentMiddleware()
        self.request.META = {
            "HTTP_USER_AGENT":
            "Mozilla/2.0 (compatible; Ask Jeeves/Teoma; +http://about.ask.com/en/docs/about/webmasters.shtml)"
        }
        self.assertEqual(self.middleware.process_request(self.request), None)

    @override_settings(
        USER_AGENTS=["TestUserAgent", ],
        BACKEND='django_seo_js.backends.TestBackend'
    )
    def test_missing_user_agent_still_works(self):
        self.middleware = UserAgentMiddleware()
        self.request.META = {}
        self.assertEqual(self.middleware.process_request(self.request), None)

    @override_settings(BACKEND='django_seo_js.backends.TestBackend', ENABLED=False)
    def test_overriding_matches_skips_if_disabled_via_enabled(self):
        self.middleware = UserAgentMiddleware()
        self.request.META = {
            "HTTP_USER_AGENT": "The TestUserAgent v1.0"
        }
        self.assertEqual(self.middleware.process_request(self.request), None)

    @override_settings(BACKEND='django_seo_js.backends.TestServiceDownBackend')
    def test_overriding_matches_skips_if_service_is_down(self):
        self.middleware = UserAgentMiddleware()
        self.request.META = {
            "HTTP_USER_AGENT":
            "Mozilla/2.0 (compatible; Ask Jeeves/Teoma; +http://about.ask.com/en/docs/about/webmasters.shtml)"
        }
        self.assertEqual(self.middleware.process_request(self.request), None)

    @override_settings(BACKEND='django_seo_js.backends.TestBackend')
    def test_overriding_skips_sitemap_xml_by_default(self):
        self.middleware = UserAgentMiddleware()
        self.request.path = "/sitemap.xml"
        self.request.META = {
            "HTTP_USER_AGENT":
            "Mozilla/2.0 (compatible; Ask Jeeves/Teoma; +http://about.ask.com/en/docs/about/webmasters.shtml)"
        }
        self.assertEqual(self.middleware.process_request(self.request), None)

    @override_settings(
        BACKEND='django_seo_js.backends.TestBackend',
        IGNORE_URLS=["/foo.html", "/bar/ibbity.html", ],
        IGNORE_EXTENSIONS=[],
    )
    def test_overriding_skips_custom_overrides_xml_by_default(self):
        self.middleware = UserAgentMiddleware()
        self.request.path = "/sitemap.xml"
        self.request.META = {
            "HTTP_USER_AGENT":
            "Mozilla/2.0 (compatible; Ask Jeeves/Teoma; +http://about.ask.com/en/docs/about/webmasters.shtml)"
        }
        self.assertEqual(self.middleware.process_request(self.request).content, b"Test")

        self.request.path = "/foo.html"
        self.assertEqual(self.middleware.process_request(self.request), None)

        self.request.path = "/bar/ibbity.html"
        self.assertEqual(self.middleware.process_request(self.request), None)

    @override_settings(BACKEND='django_seo_js.backends.TestBackend')
    def test_overriding_skips_gifs_by_default(self):
        self.middleware = UserAgentMiddleware()
        self.request.path = "/foo.gif"
        self.request.META = {
            "HTTP_USER_AGENT":
            "Mozilla/2.0 (compatible; Ask Jeeves/Teoma; +http://about.ask.com/en/docs/about/webmasters.shtml)"
        }
        self.assertEqual(self.middleware.process_request(self.request), None)

    @override_settings(
        BACKEND='django_seo_js.backends.TestBackend',
        IGNORE_EXTENSIONS=[".html", ".txt", ]
    )
    def test_overriding_skips_custom_overrides_gifs_by_default(self):
        self.middleware = UserAgentMiddleware()
        self.request.path = "/foo.gif"
        self.request.META = {
            "HTTP_USER_AGENT":
            "Mozilla/2.0 (compatible; Ask Jeeves/Teoma; +http://about.ask.com/en/docs/about/webmasters.shtml)"
        }
        self.assertEqual(self.middleware.process_request(self.request).content, b"Test")

        self.request.path = "/foo.html"
        self.assertEqual(self.middleware.process_request(self.request), None)

        self.request.path = "/bar/ibbity.txt"
        self.assertEqual(self.middleware.process_request(self.request), None)
