from django_seo_js import settings
from django_seo_js.backends import SelectedBackend


def update_cache_for_url(url):
    if settings.ENABLED:
        selector = SelectedBackend()
        return selector.backend.update_url(url)
    return False


def request_should_be_ignored(request):
    for url in settings.IGNORE_URLS:
        if url in request.path:
            return True

    extension = None
    last_dot = request.path.rfind(".")
    if last_dot == -1:
        # No extension found
        return False

    extension = request.path[last_dot:]
    return extension and extension in settings.IGNORE_EXTENSIONS
