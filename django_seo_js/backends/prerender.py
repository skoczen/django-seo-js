from django.conf import settings
from base import SEOBackendBase, RequestsBasedBackend


class PrerenderIO(SEOBackendBase, RequestsBasedBackend):
    """Implements the backend for prerender.io"""
    BASE_URL = "http://service.prerender.io/"
    RECACHE_URL = "http://api.prerender.io/recache"

    def __init__(self, *args, **kwargs):
        super(SEOBackendBase, self).__init__(*args, **kwargs)
        self.token = self._get_token()

    def _get_token(self):
        if not getattr(settings, "SEO_JS_PRERENDER_TOKEN"):
            raise ValueError("Missing SEO_JS_PRERENDER_TOKEN in settings.")
        return settings.SEO_JS_PRERENDER_TOKEN

    def get_response_for_url(self, url):
        """
        Accepts a fully-qualified url.
        Returns an HttpResponse, passing through all headers and the status code.
        """

        if not url or "//" not in url:
            raise ValueError("Missing or invalid url: %s" % url)
        render_url = "%s%s" % (self.BASE_URL, url)
        headers = {
            'X-Prerender-Token': self.token,
            'Accept-Encoding': 'gzip',
        }
        r = self.requests.get(render_url, headers=headers)
        assert int(r.status_code) < 500

        return self.build_django_response_from_requests_response(r)

    def update_url(self, url=None, regex=None):
        """
        Accepts a fully-qualified url, or regex.
        Returns True if successful, False if not successful.
        """

        if not url and not regex:
            raise ValueError("Neither a url or regex was provided to update_url.")

        headers = {
            'X-Prerender-Token': self.token,
            'Content-type': 'application/json',
            'Accept-Encoding': 'gzip',
        }
        data = {
            'prerenderToken': settings.SEO_JS_PRERENDER_TOKEN,
        }
        if url:
            data["url"] = url
        if regex:
            data["regex"] = regex

        r = self.requests.post(self.RECACHE_URL, headers=headers, data=data)
        return int(r.status_code) < 500


class PrerenderHosted(PrerenderIO):
    """Implements the backend for an arbitrary prerender service
       specified in settings.SEO_JS_PRERENDER_URL"""

    def __init__(self, *args, **kwargs):
        super(SEOBackendBase, self).__init__(*args, **kwargs)
        self.token = ""
        if not getattr(settings, "SEO_JS_PRERENDER_URL", None):
            raise ValueError("Missing SEO_JS_PRERENDER_URL in settings.")
        if not getattr(settings, "SEO_JS_PRERENDER_RECACHE_URL", None):
            raise ValueError("Missing SEO_JS_PRERENDER_RECACHE_URL in settings.")

        self.BASE_URL = getattr(settings, "SEO_JS_PRERENDER_URL")
        self.RECACHE_URL = getattr(settings, "SEO_JS_PRERENDER_RECACHE_URL")

    def _get_token(self):
        pass
