from django_seo_js.backends import SelectedBackend


class HashBangMiddleware(SelectedBackend):
    def process_request(self, request):
        if "_escaped_fragment_" in request.GET:
            url = "%s://%s%s" % (request.protocol, request.host, request.uri)
            return self.backend.get_rendered_page(url)
