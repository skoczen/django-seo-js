django-seo-js
=============

Django-seo-js is a drop-in app that provides full SEO support for angular, backbone, ember, famo.us, or other SPA apps built with django.

It's simple to set up, configurable to use multiple services, and easy to customize.

Quick-links:
- [Installation](README.md#installation)
- [Options](README.md#options)
    - [Settings](README.md#Settings)
    - [Backends](README.md#backends)
    - [Details](README.md#details)
- [Releases](README.md#releases)


# Installation

Pip install

```bash
pip install django-seo-js
```


Add to your settings.py:

```python
MIDDLEWARE_CLASSES = (
    'django_seo_js.middleware.HashBangMiddleware',  # If you're using #!
    'django_seo_js.middleware.UserAgentMiddleware',  # If you want to detect by user agent
) + MIDDLEWARE_CLASSES


SEO_JS_BACKEND = "django_seo_js.backends.PrerenderIO"   # Default
SEO_JS_PRERENDERIO_API_KEY = "123189jlisadflkaskjflka"
```

Add this to your base.html

```html
{% load django_seo_js %}
<head>
    {% seo_js_head %}
    ...
</head>
```

That's it!


# Options

## Settings

```python
SEO_JS_BACKEND = "django_seo_js.backends.PrerenderIO"   # Default
SEO_JS_PRERENDERIO_API_KEY = "123189jlisadflkaskjflka"
```


## Backends

#### Prerender.io
Django-seo-js defaults to using prerender.io because it's both open-source *and* really reasonably priced.

Using prerender.io

- Set KEY
- Leave BACKEND as default

Using your own

- Set URL

## Details

- Hashbang vs user-agent




# Releases

### 0.1 - May 8, 2014

* First release - we're using this in production at http://greenkahuna.com.

