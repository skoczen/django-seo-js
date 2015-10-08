from django_seo_js import settings
from django_seo_js.backends import SelectedBackend
from django_seo_js.helpers import request_should_be_ignored

import logging
logger = logging.getLogger(__name__)


class EscapedFragmentMiddleware(SelectedBackend):
    def process_request(self, request):
        if not settings.ENABLED:
            return

        if request_should_be_ignored(request):
            return

        if "_escaped_fragment_" not in request.GET:
            return

        url = self.backend.build_absolute_uri(request)
        try:
            return self.backend.get_response_for_url(url, request)
        except Exception as e:
            logger.exception(e)


class HashBangMiddleware(EscapedFragmentMiddleware):

    def __init__(self, *args, **kwargs):
        logging.info(
            "Deprecation note: HashBangMiddleware has been renamed EscapedFragmentMiddleware,"
            " for more clarity. Upgrade your MIDDLEWARE_CLASSES to \n"
            "   'django_seo_js.middleware.EscapedFragmentMiddleware'"
            " when you get a chance. HashBangMiddleware will be removed in v0.5"
        )
        super(HashBangMiddleware, self).__init__(*args, **kwargs)
