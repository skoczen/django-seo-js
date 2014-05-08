import re
from django.conf import settings
from .backends import SelectedBackend

DEFAULT_SEO_JS_USER_AGENTS = [
    "Googlebot",
    "Yahoo",
    "bingbot",
    "Badiu",
    "Ask Jeeves",
]


class HashBangMiddleware(SelectedBackend):
    def process_request(self, request):
        if request.GET.get("_escaped_fragment_", None):
            url = "%s://%s%s" % (self.request.protocol, self.request.host, self.request.uri)
            return self.backend.get_rendered_page(url)


class UserAgentMiddleware(SelectedBackend):
    def __init__(self, *args, **kwargs):
        super(UserAgentMiddleware, self).__init__(*args, **kwargs)
        if settings.get("SEO_JS_USER_AGENTS", None):
            agents = settings.get("SEO_JS_USER_AGENTS")
        else:
            agents = DEFAULT_SEO_JS_USER_AGENTS

        regex_str = "|".join(agents)
        regex_str = ".*?(%s)" % regex_str
        self.USER_AGENT_REGEX = re.compile(regex_str)

    def process_request(self, request):
        if self.USER_AGENT_REGEX.match(request.META["HTTP_USER_AGENT"]):
            url = "%s://%s%s" % (self.request.protocol, self.request.host, self.request.uri)
            return self.backend.get_rendered_page(url)
