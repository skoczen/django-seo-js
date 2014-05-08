
from django_seo_js.backends import SelectedBackend

def update_cache_for_url(url):
    selector = SelectedBackend()
    return selector.backend.update_url(url)
