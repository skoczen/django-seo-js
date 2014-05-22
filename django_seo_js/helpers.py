from django.conf import settings
from django_seo_js.backends import SelectedBackend


def update_cache_for_url(url):
    if getattr(settings, "SEO_JS_ENABLED", not settings.DEBUG):
        selector = SelectedBackend()
        return selector.backend.update_url(url)
    return False


def request_should_be_ignored(request):
    # TODO: move these to a central settings/default area ala appconf.
    if getattr(settings, "SEO_JS_IGNORE_URLS", None):
        IGNORE_URLS = settings.SEO_JS_IGNORE_URLS
    else:
        IGNORE_URLS = ["/sitemap.xml", ]

    ignore = False
    for url in IGNORE_URLS:
        if url in request.path:
            ignore = True
            break

    return ignore