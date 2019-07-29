from django.conf import settings as django_settings

ENABLED = getattr(django_settings, 'SEO_JS_ENABLED', not django_settings.DEBUG)

IGNORE_URLS = frozenset(getattr(django_settings, 'SEO_JS_IGNORE_URLS', ['/sitemap.xml']))

IGNORE_EXTENSIONS = frozenset(getattr(django_settings, 'SEO_JS_IGNORE_EXTENSIONS', (
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
    ".torrent",
)))

USER_AGENTS = frozenset(getattr(django_settings, 'SEO_JS_USER_AGENTS', (
    # These first three should be disabled, since they support escaped fragments, and
    # and leaving them enabled will penalize a website as "cloaked".
    # "Googlebot",
    # "Yahoo",
    # "bingbot",

    "Ask Jeeves",
    "baiduspider",
    "facebookexternalhit",
    "twitterbot",
    "rogerbot",
    "linkedinbot",
    "embedly",
    "quoralink preview'",
    "showyoubot",
    "outbrain",
    "pinterest",
    "developersgoogle.com/+/web/snippet",
)))

BACKEND = getattr(django_settings, 'SEO_JS_BACKEND', 'django_seo_js.backends.PrerenderIO')

PRERENDER_TOKEN = getattr(django_settings, 'SEO_JS_PRERENDER_TOKEN', None)
PRERENDER_URL = getattr(django_settings, 'SEO_JS_PRERENDER_URL', None)
PRERENDER_RECACHE_URL = getattr(django_settings, 'SEO_JS_PRERENDER_RECACHE_URL', None)

SEND_USER_AGENT = getattr(django_settings, 'SEO_JS_SEND_USER_AGENT', True)
