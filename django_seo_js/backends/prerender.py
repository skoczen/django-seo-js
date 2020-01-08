from django_seo_js import settings
from .base import SEOBackendBase, RequestsBasedBackend


class PrerenderIO(SEOBackendBase, RequestsBasedBackend):
    """Implements the backend for prerender.io"""
    BASE_URL = "https://service.prerender.io/"
    RECACHE_URL = "https://api.prerender.io/recache"

    def __init__(self, *args, **kwargs):
        super(SEOBackendBase, self).__init__(*args, **kwargs)
        self.token = self._get_token()

    def _get_token(self):
        if settings.PRERENDER_TOKEN is None:
            raise ValueError("Missing SEO_JS_PRERENDER_TOKEN in settings.")
        return settings.PRERENDER_TOKEN

    def get_response_for_url(self, url, request=None):
        """
        Accepts a fully-qualified url.
        Returns an HttpResponse, passing through all headers and the status code.
        """

        if not url or "//" not in url:
            raise ValueError("Missing or invalid url: %s" % url)

        render_url = self.BASE_URL + url
        headers = {
            'X-Prerender-Token': self.token,
        }
        if request and settings.SEND_USER_AGENT:
            headers.update({'User-Agent': request.META.get('HTTP_USER_AGENT')})

        r = self.session.get(render_url, headers=headers, allow_redirects=False)
        assert r.status_code < 500

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
            'Content-Type': 'application/json',
        }
        data = {
            'prerenderToken': settings.PRERENDER_TOKEN,
        }
        if url:
            data["url"] = url
        if regex:
            data["regex"] = regex

        r = self.session.post(self.RECACHE_URL, headers=headers, data=data)
        return r.status_code < 500


class PrerenderHosted(PrerenderIO):
    """Implements the backend for an arbitrary prerender service
       specified in settings.SEO_JS_PRERENDER_URL"""

    def __init__(self, *args, **kwargs):
        super(SEOBackendBase, self).__init__(*args, **kwargs)
        self.token = ""
        if not settings.PRERENDER_URL:
            raise ValueError("Missing SEO_JS_PRERENDER_URL in settings.")
        if not settings.PRERENDER_RECACHE_URL:
            raise ValueError("Missing SEO_JS_PRERENDER_RECACHE_URL in settings.")

        self.BASE_URL = settings.PRERENDER_URL
        self.RECACHE_URL = settings.PRERENDER_RECACHE_URL

    def _get_token(self):
        pass

    def update_url(self, url=None):
        """
        Accepts a fully-qualified url.
        Returns True if successful, False if not successful.
        """
        if not url:
            raise ValueError("Neither a url or regex was provided to update_url.")
        post_url = "%s%s" % (self.BASE_URL, url)
        r = self.session.post(post_url)
        return int(r.status_code) < 500
