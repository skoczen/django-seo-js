import re
from django.conf import settings
from django_seo_js.backends import SelectedBackend
from django_seo_js.helpers import request_should_be_ignored


DEFAULT_SEO_JS_USER_AGENTS = [
    "Googlebot",
    "Yahoo",
    "bingbot",
    "Ask Jeeves",
    "baiduspider",
    "facebookexternalhit",
    "twitterbot",
    "rogerbot",
    "linkedinbot",
    "embedly",
    "quoralink preview'",
    "showyoubot",
    "outbrain",
    "pinterest",
    "developersgoogle.com/+/web/snippet",
]


class UserAgentMiddleware(SelectedBackend):
    def __init__(self, *args, **kwargs):
        super(UserAgentMiddleware, self).__init__(*args, **kwargs)
        if getattr(settings, "SEO_JS_USER_AGENTS", None):
            agents = getattr(settings, "SEO_JS_USER_AGENTS")
        else:
            agents = DEFAULT_SEO_JS_USER_AGENTS
        regex_str = "|".join(agents)
        regex_str = ".*?(%s)" % regex_str
        self.USER_AGENT_REGEX = re.compile(regex_str, re.IGNORECASE)

    def process_request(self, request):
        # TODO: move to proper settings app pattern.
        if (
            not request_should_be_ignored(request) and
            getattr(settings, "SEO_JS_ENABLED", not settings.DEBUG) and
            "HTTP_USER_AGENT" in request.META and
            self.USER_AGENT_REGEX.match(request.META["HTTP_USER_AGENT"])
        ):

            url = request.build_absolute_uri()

            try:
                return self.backend.get_response_for_url(url)
            except:
                pass
