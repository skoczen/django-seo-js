from django.conf import settings
from django_seo_js.backends import SelectedBackend


def update_cache_for_url(url):
    if getattr(settings, "SEO_JS_ENABLED", not settings.DEBUG):
        selector = SelectedBackend()
        return selector.backend.update_url(url)
    return False
