from django_seo_js.backends import SelectedBackend
from django.http import HttpResponse


class HashBangMiddleware(SelectedBackend):
    def process_request(self, request):
        if "_escaped_fragment_" in request.GET:
            url = request.build_absolute_uri()
            return HttpResponse(self.backend.get_rendered_page(url))
