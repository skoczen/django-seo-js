import importlib
import requests
from django.conf import settings
from django.http import HttpResponse


DEFAULT_BACKEND = "django_seo_js.backends.PrerenderIO"
IGNORED_HEADERS = [
    'connection', 'keep-alive', 'proxy-authenticate',
    'proxy-authorization', 'te', 'trailers', 'transfer-encoding',
    'upgrade', 'content-length', 'content-encoding'
]


class SelectedBackend(object):

    def __init__(self, *args, **kwargs):
        if getattr(settings, "SEO_JS_BACKEND", None):
            module_path = getattr(settings, "SEO_JS_BACKEND")
        else:
            module_path = DEFAULT_BACKEND

        backend_module = importlib.import_module(".".join(module_path.split(".")[:-1]))
        self.backend = getattr(backend_module, module_path.split(".")[-1])()


class SEOBackendBase(object):
    """The base class to inherit for SEO_JS backends"""

    def get_response_for_url(self, url):
        """
        Accepts a fully-qualified url.
        Returns an HttpResponse, passing through all headers and the status code.
        """
        raise NotImplementedError

    def update_url(self, url):
        """
        Force an update of the cache for a particular URL.
        Returns True on success, False on fail.
        """
        raise NotImplementedError


class RequestsBasedBackend(object):

    def __init__(self, *args, **kwargs):
        super(RequestsBasedBackend, self).__init__(*args, **kwargs)
        self.requests = requests

    def build_django_response_from_requests_response(self, response):
        r = HttpResponse(response.content)
        for k, v in response.headers.items():
            if k not in IGNORED_HEADERS:
                r[k] = v
        r['content-length'] = len(response.content)
        r.status_code = response.status_code
        return r
