from django.conf import settings
import importlib


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

    def update_url(self, url):
        """Force an update of the cache for a particular URL."""
        raise NotImplementedError