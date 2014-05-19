from django_seo_js.backends import SelectedBackend
from django.conf import settings


class HashBangMiddleware(SelectedBackend):
    def process_request(self, request):
        print "request"
        if getattr(settings, "SEO_JS_ENABLED", not settings.DEBUG) and "_escaped_fragment_" in request.GET:

            url = request.build_absolute_uri()
            print url
            try:
                return self.backend.get_response_for_url(url)
            except:
                pass
