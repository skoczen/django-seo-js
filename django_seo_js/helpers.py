import fnmatch
import re
from django_seo_js import settings
from django_seo_js.backends import SelectedBackend


def update_cache_for_url(url):
    if settings.ENABLED:
        selector = SelectedBackend()
        return selector.backend.update_url(url)
    return False


def request_should_be_ignored(request):
    if settings.ALLOWED_URLS:
        return not request_in_allowed_url_list(request)

    return request_in_ignore_url_list(request) or request_in_ingore_extensions_list(request)


def request_in_ignore_url_list(request):
    for url in settings.IGNORE_URLS:
        if url in request.path:
            return True

    return False


def request_in_ingore_extensions_list(request):
    extension = None
    last_dot = request.path.rfind(".")
    if last_dot == -1:
        # No extension found
        return False

    extension = request.path[last_dot:]
    return extension and extension in settings.IGNORE_EXTENSIONS


def request_in_allowed_url_list(request):
    for pattern in settings.ALLOWED_URLS:
        regex = fnmatch.translate(pattern)
        re_obj = re.compile(regex)
        if re_obj.match(request.path):
            return True

    return False
