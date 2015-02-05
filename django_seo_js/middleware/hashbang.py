from django_seo_js import settings
from django_seo_js.backends import SelectedBackend
from django_seo_js.helpers import request_should_be_ignored

import logging
logger = logging.getLogger(__name__)


class HashBangMiddleware(SelectedBackend):
    def process_request(self, request):
        if not settings.ENABLED:
            return

        if request_should_be_ignored(request):
            return

        if "_escaped_fragment_" not in request.GET:
            return

        url = request.build_absolute_uri()
        try:
            return self.backend.get_response_for_url(url)
        except Exception as e:
            logger.exception(e)
