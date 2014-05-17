import re
from django.conf import settings
from django_seo_js.backends import SelectedBackend
from django.http import HttpResponse

DEFAULT_SEO_JS_USER_AGENTS = [
    "Googlebot",
    "Yahoo",
    "bingbot",
    "Badiu",
    "Ask Jeeves",
]
# TODO Next steps:
# 1. Pull this into its own file
# 2. Write unit tests for it
# 3. Make sure we have a clear abstraction and inheritance.
class DjangoSeoJSMiddlewareHelpers(object):

    def build_django_response_from_requests_response(self, response):
        raise NotImplementedError

        r = HttpResponse(content)
        for k, v in r.headers.items():
            r[k] = v
        r.status_code = response.status_code
        r.content_type = response.content_type
        return r


class UserAgentMiddleware(SelectedBackend, DjangoSeoJSMiddlewareHelpers):
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
        if (getattr(settings, "SEO_JS_ENABLED", not settings.DEBUG) and
            "HTTP_USER_AGENT" in request.META and
            self.USER_AGENT_REGEX.match(request.META["HTTP_USER_AGENT"])):

            url = request.build_absolute_uri()

            result = None
            try:
                result = self.backend.get_rendered_page(url)
            except:
                pass

            if self.valid_backend_result(result):
                # Which calls
                return self.build_django_response_from_requests_response(r)

