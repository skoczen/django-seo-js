from django.conf import settings
from django_seo_js.backends import SelectedBackend


DEFAULT_IGNORED_EXTENSIONS = [
    ".js",
    ".css",
    ".xml",
    ".less",
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".pdf",
    ".doc",
    ".txt",
    ".ico",
    ".rss",
    ".zip",
    ".mp3",
    ".rar",
    ".exe",
    ".wmv",
    ".doc",
    ".avi",
    ".ppt",
    ".mpg",
    ".mpeg",
    ".tif",
    ".wav",
    ".mov",
    ".psd",
    ".ai",
    ".xls",
    ".mp4",
    ".m4a",
    ".swf",
    ".dat",
    ".dmg",
    ".iso",
    ".flv",
    ".m4v",
    ".torrent"
]


def update_cache_for_url(url):
    if getattr(settings, "SEO_JS_ENABLED", not settings.DEBUG):
        selector = SelectedBackend()
        return selector.backend.update_url(url)
    return False


def request_should_be_ignored(request):
    # TODO: move these to a central settings/default area ala appconf.
    # Note it's tougher than it looks because of the override_settings
    # magical injection in tests.
    if getattr(settings, "SEO_JS_IGNORE_URLS", None):
        IGNORE_URLS = settings.SEO_JS_IGNORE_URLS
    else:
        IGNORE_URLS = ["/sitemap.xml", ]

    ignore = False
    for url in IGNORE_URLS:
        if url in request.path:
            ignore = True
            break

    if not ignore:
        if getattr(settings, "SEO_JS_IGNORE_EXTENSIONS", None) is not None:
            IGNORED_EXTENSIONS = settings.SEO_JS_IGNORE_EXTENSIONS
        else:
            IGNORED_EXTENSIONS = DEFAULT_IGNORED_EXTENSIONS
        extension = None
        last_dot = request.path.rfind(".")
        if last_dot != -1:
            extension = request.path[last_dot:]
        if extension:
            for ext in IGNORED_EXTENSIONS:
                if extension == ext:
                    ignore = True
                    break

    return ignore