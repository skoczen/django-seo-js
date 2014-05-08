import re
from django.conf import settings
from django_seo_js.backends import SelectedBackend

DEFAULT_SEO_JS_USER_AGENTS = [
    "Googlebot",
    "Yahoo",
    "bingbot",
    "Badiu",
    "Ask Jeeves",
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
        if self.USER_AGENT_REGEX.match(request.META["HTTP_USER_AGENT"]):
            url = "%s://%s%s" % (request.protocol, request.host, request.uri)
            return self.backend.get_rendered_page(url)
