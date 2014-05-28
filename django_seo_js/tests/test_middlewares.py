from mock import Mock
from django.test import TestCase
from django.test.utils import override_settings

from django_seo_js.middleware import HashBangMiddleware, UserAgentMiddleware


class BaseMiddlewareTest(TestCase):
    pass


class HashBangMiddlewareTest(TestCase):

    @override_settings(SEO_JS_BACKEND='django_seo_js.backends.TestBackend')
    def setUp(self):
        super(HashBangMiddlewareTest, self).setUp()
        self.middleware = HashBangMiddleware()
        self.request = Mock()
        self.request.path = "/"
        self.request.GET = {}

    def test_has_escaped_fragment(self):
        self.request.GET = {"_escaped_fragment_": None}
        self.assertEqual(self.middleware.process_request(self.request).content, "Test")

    def test_does_not_have_escaped_fragment(self):
        self.request.GET = {}
        self.assertEqual(self.middleware.process_request(self.request), None)

    @override_settings(SEO_JS_BACKEND='django_seo_js.backends.TestBackend', DEBUG=True)
    def test_has_escaped_fragment_skips_if_disabled_via_debug(self):
        self.middleware = HashBangMiddleware()
        self.request.GET = {}
        self.assertEqual(self.middleware.process_request(self.request), None)

    @override_settings(SEO_JS_BACKEND='django_seo_js.backends.TestBackend', SEO_JS_ENABLED=False)
    def test_has_escaped_fragment_skips_if_disabled_via_enabled(self):
        self.middleware = HashBangMiddleware()
        self.request.GET = {}
        self.assertEqual(self.middleware.process_request(self.request), None)

    @override_settings(SEO_JS_BACKEND='django_seo_js.backends.TestServiceDownBackend')
    def test_has_escaped_fragment_skips_if_service_is_down(self):
        self.middleware = HashBangMiddleware()
        self.request.GET = {"_escaped_fragment_": None}
        self.assertEqual(self.middleware.process_request(self.request), None)

    @override_settings(SEO_JS_BACKEND='django_seo_js.backends.TestBackend')
    def test_overriding_skips_sitemap_xml_by_default(self):
        self.middleware = HashBangMiddleware()
        self.request.path = "/sitemap.xml"
        self.request.GET = {"_escaped_fragment_": None}
        self.assertEqual(self.middleware.process_request(self.request), None)

    @override_settings(
        SEO_JS_BACKEND='django_seo_js.backends.TestBackend',
        SEO_JS_IGNORE_URLS=["/foo.html", "/bar/ibbity.html", ],
        SEO_JS_IGNORE_EXTENSIONS=[],
    )
    def test_overriding_skips_custom_overrides_xml_by_default(self):
        self.middleware = HashBangMiddleware()
        self.request.path = "/sitemap.xml"
        self.request.GET = {"_escaped_fragment_": None}
        self.assertEqual(self.middleware.process_request(self.request).content, "Test")

        self.request.path = "/foo.html"
        self.assertEqual(self.middleware.process_request(self.request), None)

        self.request.path = "/bar/ibbity.html"
        self.assertEqual(self.middleware.process_request(self.request), None)

    @override_settings(SEO_JS_BACKEND='django_seo_js.backends.TestBackend')
    def test_overriding_skips_gifs_by_default(self):
        self.middleware = HashBangMiddleware()
        self.request.path = "/sitemap.xml"
        self.request.GET = {"_escaped_fragment_": None}
        self.assertEqual(self.middleware.process_request(self.request), None)

    @override_settings(
        SEO_JS_BACKEND='django_seo_js.backends.TestBackend',
        SEO_JS_IGNORE_EXTENSIONS=[".html", ".txt", ]
    )
    def test_overriding_skips_custom_overrides_gifs_by_default(self):
        self.middleware = HashBangMiddleware()
        self.request.path = "/foo.gif"
        self.request.GET = {"_escaped_fragment_": None}
        self.assertEqual(self.middleware.process_request(self.request).content, "Test")

        self.request.path = "/foo.html"
        self.assertEqual(self.middleware.process_request(self.request), None)

        self.request.path = "/bar/ibbity.txt"
        self.assertEqual(self.middleware.process_request(self.request), None)


class UserAgentMiddlewareTest(TestCase):

    @override_settings(SEO_JS_BACKEND='django_seo_js.backends.TestBackend')
    def setUp(self):
        super(UserAgentMiddlewareTest, self).setUp()
        self.middleware = UserAgentMiddleware()
        self.request = Mock()
        self.request.path = "/"
        self.request.META = {}

    def test_matches_one_of_the_default_user_agents(self):
        self.request.META = {
            "HTTP_USER_AGENT": "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"
        }
        self.assertEqual(self.middleware.process_request(self.request).content, "Test")

    def test_does_not_match_one_of_the_default_user_agents(self):
        self.request.META = {
            "HTTP_USER_AGENT": "This user-agent is not a search engine."
        }
        self.assertEqual(self.middleware.process_request(self.request), None)

    @override_settings(
        SEO_JS_USER_AGENTS=["TestUserAgent", ],
        SEO_JS_BACKEND='django_seo_js.backends.TestBackend'
    )
    def test_overriding_matches(self):
        self.middleware = UserAgentMiddleware()
        self.request.META = {
            "HTTP_USER_AGENT": "The TestUserAgent v1.0"
        }
        self.assertEqual(self.middleware.process_request(self.request).content, "Test")

    @override_settings(
        SEO_JS_USER_AGENTS=["TestUserAgent", ],
        SEO_JS_BACKEND='django_seo_js.backends.TestBackend'
    )
    def test_overriding_does_not_match_properly(self):
        self.middleware = UserAgentMiddleware()
        self.request.META = {
            "HTTP_USER_AGENT": "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"
        }
        self.assertEqual(self.middleware.process_request(self.request), None)

    @override_settings(
        SEO_JS_USER_AGENTS=["TestUserAgent", ],
        SEO_JS_BACKEND='django_seo_js.backends.TestBackend'
    )
    def test_missing_user_agent_still_works(self):
        self.middleware = UserAgentMiddleware()
        self.request.META = {}
        self.assertEqual(self.middleware.process_request(self.request), None)

    @override_settings(SEO_JS_BACKEND='django_seo_js.backends.TestBackend', DEBUG=True)
    def test_overriding_matches_skips_if_disabled_via_debug(self):
        self.middleware = UserAgentMiddleware()
        self.request.META = {
            "HTTP_USER_AGENT": "The TestUserAgent v1.0"
        }
        self.assertEqual(self.middleware.process_request(self.request), None)

    @override_settings(SEO_JS_BACKEND='django_seo_js.backends.TestBackend', SEO_JS_ENABLED=False)
    def test_overriding_matches_skips_if_disabled_via_enabled(self):
        self.middleware = UserAgentMiddleware()
        self.request.META = {
            "HTTP_USER_AGENT": "The TestUserAgent v1.0"
        }
        self.assertEqual(self.middleware.process_request(self.request), None)

    @override_settings(SEO_JS_BACKEND='django_seo_js.backends.TestServiceDownBackend')
    def test_overriding_matches_skips_if_service_is_down(self):
        self.middleware = UserAgentMiddleware()
        self.request.META = {
            "HTTP_USER_AGENT": "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"
        }
        self.assertEqual(self.middleware.process_request(self.request), None)

    @override_settings(SEO_JS_BACKEND='django_seo_js.backends.TestBackend')
    def test_overriding_skips_sitemap_xml_by_default(self):
        self.middleware = UserAgentMiddleware()
        self.request.path = "/sitemap.xml"
        self.request.META = {
            "HTTP_USER_AGENT": "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"
        }
        self.assertEqual(self.middleware.process_request(self.request), None)

    @override_settings(
        SEO_JS_BACKEND='django_seo_js.backends.TestBackend',
        SEO_JS_IGNORE_URLS=["/foo.html", "/bar/ibbity.html", ],
        SEO_JS_IGNORE_EXTENSIONS=[],
    )
    def test_overriding_skips_custom_overrides_xml_by_default(self):
        self.middleware = UserAgentMiddleware()
        self.request.path = "/sitemap.xml"
        self.request.META = {
            "HTTP_USER_AGENT": "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"
        }
        self.assertEqual(self.middleware.process_request(self.request).content, "Test")

        self.request.path = "/foo.html"
        self.assertEqual(self.middleware.process_request(self.request), None)

        self.request.path = "/bar/ibbity.html"
        self.assertEqual(self.middleware.process_request(self.request), None)

    @override_settings(SEO_JS_BACKEND='django_seo_js.backends.TestBackend')
    def test_overriding_skips_gifs_by_default(self):
        self.middleware = UserAgentMiddleware()
        self.request.path = "/foo.gif"
        self.request.META = {
            "HTTP_USER_AGENT": "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"
        }
        self.assertEqual(self.middleware.process_request(self.request), None)

    @override_settings(
        SEO_JS_BACKEND='django_seo_js.backends.TestBackend',
        SEO_JS_IGNORE_EXTENSIONS=[".html", ".txt", ]
    )
    def test_overriding_skips_custom_overrides_gifs_by_default(self):
        self.middleware = UserAgentMiddleware()
        self.request.path = "/foo.gif"
        self.request.META = {
            "HTTP_USER_AGENT": "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"
        }
        self.assertEqual(self.middleware.process_request(self.request).content, "Test")

        self.request.path = "/foo.html"
        self.assertEqual(self.middleware.process_request(self.request), None)

        self.request.path = "/bar/ibbity.txt"
        self.assertEqual(self.middleware.process_request(self.request), None)
