from django.http import HttpResponse

from base import SEOBackendBase


class TestBackend(SEOBackendBase):
    """Implements a test backend"""

    def get_response_for_url(self, url):
        r = HttpResponse("Test")
        r["test rendered"] = "headers"
        r.status_code = 200
        r.content_type = "text/html"
        return r

    def update_url(self, url):
        return True


class TestServiceDownBackend(SEOBackendBase):
    """Implements a test backend"""

    def get_response_for_url(self, url):
        r = HttpResponse("Service Down")
        r["test rendered"] = "headers"
        r.status_code = 503
        r.content_type = "text/html"
        assert r.status_code < 500

    def update_url(self, url):
        return False
