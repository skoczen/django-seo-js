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
    path = request.path
    if settings.IGNORE_URLS and is_path_in_black_list(path):
        # black list is enabled and path is in the black list
        return True

    if settings.IGNORE_EXTENSIONS and is_path_in_ignore_extensions_list(path):
        return True

    if settings.ALLOWED_URLS and not is_path_in_white_list(path):
        # white list is enabled and path is not in the white list
        return True

    return False


def is_path_in_list(path, pattern_list):
    for pattern in pattern_list:
        regex = fnmatch.translate(pattern)
        re_obj = re.compile(regex)
        if re_obj.match(path):
            return True

    return False


def is_path_in_white_list(path):
    return is_path_in_list(path, settings.ALLOWED_URLS)


def is_path_in_black_list(path):
    return is_path_in_list(path, settings.IGNORE_URLS)


def is_path_in_ignore_extensions_list(path):
    extension = None
    last_dot = path.rfind(".")
    if last_dot == -1:
        # No extension found
        return False

    extension = path[last_dot:]
    return extension and extension in settings.IGNORE_EXTENSIONS
