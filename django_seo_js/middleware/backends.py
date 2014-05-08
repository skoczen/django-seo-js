from django.conf import settings
import importlib
import requests


DEFAULT_BACKEND = "django_seo_js.backends.PrerenderIO"


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

    def get_rendered_page(self, url):
        """Accepts a fully-qualified url, returns the page body"""
        raise NotImplementedError


class PrerenderIO(SEOBackendBase):
    """Implements the backend for prerender.io"""
    BASE_URL = "http://service.prerender.io/"

    def get_rendered_page(self, url):
        """Accepts a fully-qualified url, returns the page body"""
        render_url = "%s%s" % (self.BASE_URL, url)
        r = requests.get(render_url)
        assert r.status_code == 200
        return r.content


class PrerenderHosted(PrerenderIO):
    """Implements the backend for an arbitrary prerender service
       specified in settings.SEO_JS_PRERENDER_URL"""
    BASE_URL = getattr(settings, "SEO_JS_PRERENDER_URL", None)


class TestBackend(SEOBackendBase):
    """Implements a test backend"""

    def get_rendered_page(self, url):
        return "Test"