from django.conf import settings
import requests
from base import SEOBackendBase

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
