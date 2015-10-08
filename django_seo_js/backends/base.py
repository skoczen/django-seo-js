import importlib
import requests
from django.http import HttpResponse
from django_seo_js import settings

try:
    from django.utils.deprecation import MiddlewareMixin
except ImportError:
    MiddlewareMixin = object


IGNORED_HEADERS = frozenset((
    'connection', 'keep-alive', 'proxy-authenticate',
    'proxy-authorization', 'te', 'trailers', 'transfer-encoding',
    'upgrade', 'content-length', 'content-encoding'
))


class SelectedBackend(MiddlewareMixin):

    def __init__(self, get_response=None, *args, **kwargs):
        self.get_response = get_response
        module_path = settings.BACKEND
        backend_module = importlib.import_module(".".join(module_path.split(".")[:-1]))
        self.backend = getattr(backend_module, module_path.split(".")[-1])()


class SEOBackendBase(MiddlewareMixin):
    """The base class to inherit for SEO_JS backends"""

    def build_absolute_uri(self, request):
        """
        Return the fully-qualified url that will be pre-rendered.

        Override to customize how your URIs are built.

        e.g. to strip out all query params:
        ```
        return '{scheme}://{host}{path}'.format(
            scheme=self.scheme,
            host=self.get_host(),
            path=self.path,
        )
        ```
        """
        return request.build_absolute_uri()

    def get_response_for_url(self, url, request=None):
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
        self.session = requests.Session()

    def build_django_response_from_requests_response(self, response):
        r = HttpResponse(response.content)
        for k, v in response.headers.items():
            if k.lower() not in IGNORED_HEADERS:
                r[k] = v
        r['content-length'] = len(response.content)
        r.status_code = response.status_code
        return r
