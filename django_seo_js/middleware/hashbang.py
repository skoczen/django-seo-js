from django_seo_js.backends import SelectedBackend
from django.conf import settings
from django.http import HttpResponse


class HashBangMiddleware(SelectedBackend):
    def process_request(self, request):
        if getattr(settings, "SEO_JS_ENABLED", not settings.DEBUG) and\
            "_escaped_fragment_" in request.GET:

            url = request.build_absolute_uri()
            return HttpResponse(self.backend.get_rendered_page(url))
