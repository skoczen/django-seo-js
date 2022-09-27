django-seo-js
=============

[![Build Status](https://circleci.com/gh/skoczen/django-seo-js/tree/master.svg?style=svg&circle-token=90ca5d5cbeb2af20bc378faf1b196e6c03e69f26)](https://circleci.com/gh/skoczen/django-seo-js/tree/master) ![Pypi Badge](https://badge.fury.io/py/django-seo-js.png)   ![Downloads Badge](https://img.shields.io/pypi/dm/django-seo-js.svg)

django-seo-js is a drop-in app that provides full SEO support for angular, backbone, ember, famo.us, and other SPA apps built with django.

It's simple to set up, configurable to use multiple services, and easy to customize.

Quick-links:
- [Installation](#installation)
- [Options](#options)
    - [General Settings](#General-Settings)
    - [Backend settings](#Backend-settings)
        - [Prerender.io](#Prerender-io)
        - [Custom-hosted prerender](#custom-hosted-prerender)
- [Advanced Usage](#advanced-usage)
    - [Updating the render cache](#updating-the-render-cache)
- [How it all works](#how-it-all-works)
- [Contributing](#contributing)
    - [Code](#code)
    - [Culture](#culture)
- [Authors](#authors)
- [Releases](#releases)


# Installation

1. Pip install:

    ```bash
    pip install django-seo-js
    ```


2. Add to your `settings.py`:

    ```python
    # If in doubt, just include both.  Details below.
    MIDDLEWARE_CLASSES = (
        'django_seo_js.middleware.EscapedFragmentMiddleware',  # If you're using #!
        'django_seo_js.middleware.UserAgentMiddleware',  # If you want to detect by user agent
    ) + MIDDLEWARE_CLASSES

    INSTALLED_APPS += ('django_seo_js',)

    # If you're using prerender.io (the default backend):
    SEO_JS_PRERENDER_TOKEN = "123456789abcdefghijkl"  # Really, put this in your env, not your codebase.
    ```

3. Add to your `base.html`

    ```twig
    {% load django_seo_js %}
    <head>
        {% seo_js_head %}
        ...
    </head>
    ```

4. **That's it. :)**  Your js-heavy pages are now rendered properly to the search engines. Have a lovely day.

Want more advanced control?  Keep reading.


# Options

## General settings

For the most part, you shouldn't need to override these - we've aimed for sensible defaults.

```python
# Backend to use
SEO_JS_BACKEND = "django_seo_js.backends.PrerenderIO"   # Default

# Whether to run the middlewares and update_cache_for_url.  Useful to set False for unit testing.
SEO_JS_ENABLED = True # Defaults to *not* DEBUG.

# User-agents to render for, if you're using the UserAgentMiddleware
# Defaults to the most popular.  If you have custom needs, pull from the full list:
# http://www.useragentstring.com/pages/Crawlerlist/
SEO_JS_USER_AGENTS = [
    "Googlebot",
    "Yahoo",
    "bingbot",
    "Badiu",
    "Ask Jeeves",
]

# Urls to skip the rendering backend, and always render in-app.
# Defaults to excluding sitemap.xml.
SEO_JS_IGNORE_URLS = [
    "/sitemap.xml",
]
SEO_JS_IGNORE_EXTENSIONS = [
    ".xml",
    ".txt",
    # See helpers.py for full list of extensions ignored by default.
]

# Whether or not to pass along the original request's user agent to the prerender service. 
# Useful for analytics, understanding where requests are coming from.
SEO_JS_SEND_USER_AGENT = True
```

## Backend settings

### Prerender.io
django-seo-js defaults to using prerender.io because it's both [open-source](https://github.com/prerender/prerender) if you want to run it yourself, *and* really reasonably priced if you don't.


To use [prerender.io](http://prerender.io),

```python
# Prerender.io token
SEO_JS_PRERENDER_TOKEN = "123456789abcdefghijkl"
```

You don't need to set `SEO_JS_BACKEND`, since it defaults to `"django_seo_js.backends.PrerenderIO"`.


### Custom-hosted prerender

If you're hosting your own instance of [prerender](https://github.com/prerender/prerender), (there are [docker images](https://github.com/cerisier/docker-prerender/), for those inclined,) configuration is similar

```python
SEO_JS_BACKEND = "django_seo_js.backends.PrerenderHosted"
SEO_JS_PRERENDER_URL = "http://my-prerenderapp.com/"  # Note trailing slash.
SEO_JS_PRERENDER_RECACHE_URL = "http://my-prerenderapp.com/recache"
```

### Writing your own backend

If it's a backend for a public service, please consider submitting your backend as a PR, so everyone can benefit!

Backends must implement the following methods:

```python

class MyBackend(SEOBackendBase):

    def get_response_for_url(self, url, request=None):
        """
        Accepts a fully-qualified url.
        Optionally accepts the django request object, so that headers, etc. may be passed along to the prerenderer.
        Returns an HttpResponse, passing through all headers and the status code.
        """
        raise NotImplementedError

    def update_url(self, url):
        """
        Force an update of the cache for a particular URL.
        Returns True on success, False on fail.
        """
        raise NotImplementedError
```

If you're hitting an http endpoint, there's also the helpful `RequestsBasedBackend`, which has a `build_django_response_from_requests_response` method that transforms a [python-requests](http://docs.python-requests.org/) response to a django HttpResponse, including headers, status codes, etc.

# Advanced Usage

## Updating the render cache

If you know a page's contents have changed, some backends allow you to manually update the page cache.  `django-seo-js` provides helpers to make that easy.

```python
from django_seo_js.helpers import update_cache_for_url

update_cache_for_url("/my-url")
```

So, for instance, you might want something like:

```python
def listing_changed(sender, instance, created, **kwargs):
    update_cache_for_url("%s%s" % ("http://example.com/", reverse("listing_detail", instance.pk))

post_save.connect(listing_changed, sender=Listing)
```

## Building your own URLs for prerendering

If you need to customize the fully-qualified URL, you can subclass any backend and override the `build_absolute_uri()` method.

```python
class MyBackend(SEOBackendBase):
    def build_absolute_uri(self, request):
        """Strip out all query params:"""
        return '{scheme}://{host}{path}'.format(
            scheme=self.scheme,
            host=self.get_host(),
            path=self.path,
        )
```


# How it all works

If you're looking for a big-picture explanation of how SEO for JS-heavy apps is handled, the clearest explanation I've seen is [this StackOverflow answer](http://stackoverflow.com/a/20766253).

If even that's TL;DR for you, here's a bullet-point summary:

- If requests come in with an `_escaped_fragment_` querystring or a particular user agent, a pre-rendered HTML response is served, instead of your app.
- That pre-rendered HTML is generated by a service with a headless browser that runs your js then caches the rendered page.
- Said service is generally a third party (there are many: [prerender.io](https://prerender.io/), [Brombone](http://www.brombone.com/), [seo.js](http://getseojs.com/), [seo4ajax](http://www.seo4ajax.com/).) You can also run such a service yourself, using [prerender](https://github.com/prerender/prerender), or re-invent your own wheel for fun.


# Contributing

## Code

PRs with additional backends, bug-fixes, documentation and more are definitely welcome! 

Here's some guidelines on new code:
- Incoming code should follow PEP8 (there's a test to help out on this.)
- If you add new core-level features, write some quick docs in the README.  If you're not sure if they're needed, just ask!
- Add your name and attribution to the AUTHORS file.
- Know you have everyone's thanks for helping to make django-seo-js even better!

## Culture

Anyone is welcome to contribute to django-seo-js, regardless of skill level or experience.  To make django-seo-js the best it can be, we have one big, overriding cultural principle:

**Be kind.**

Simple.  Easy, right?

We've all been newbie coders, we've all had bad days, we've all been frustrated with libraries, we've all spoken a language we learned later in life.  In discussions with other coders, PRs, and CRs, we just give each the benefit of the doubt, listen well, and assume best intentions.  It's worked out fantastically.

This doesn't mean we don't have honest, spirited discussions about the direction to move django-seo-js forward, or how to implement a feature.  We do.  We just respect one other while we do it.  Not so bad, right? :)


# Authors

django-seo-js was originally written and is maintained by [Steven Skoczen](https://stevenskoczen.com). Since then, it's been improved by lots of people, including (alphabetically):

- [alex-mcleod](https://github.com/alex-mcleod) brought you the idea of ignoring certain urls via `SEO_JS_IGNORE_URLS`.
- [andrewebdev](https://github.com/andrewebdev) improved the user-agent list to be more comprehensive.
- [chazcb](https://github.com/chazcb) added the `build_absolute_uri` method, for subclassing in complex, generated setups.
- [denisvlr](https://github.com/denisvlr) fixed the `update_url` method.
- [mattrobenolt](https://github.com/mattrobenolt) mad things faster, better, and stronger.
- [rchrd2](https://github.com/rchrd2) fixed a breaking bug with the user agent middleware.
- [thoop](https://github.com/thoop) gave you `SEO_JS_IGNORE_EXTENSIONS`, allowing you to ignore by extension.
- [bhoop77](https://github.com/bhoop77) fixed the defaults to work wiht Googlebot's new setup.
- [varrocs](https://github.com/varrocs) updated the list of user agents to match prerender.io's current list.
- [sarahboyce](https://github.com/sarahboyce) added support for Django 4.1.



Original development was at GreenKahuna (now defunct.)

# Releases

### 0.4.1 - Sep 27, 2022
Patch middleware for Django 4.1.  [PR](https://github.com/skoczen/django-seo-js/pull/44).

### 0.4.0 - Sep 26, 2022
Adds support for Django 4.1.  [PR](https://github.com/skoczen/django-seo-js/pull/42).

### 0.3.5 - Nov 26, 2021
Adds more default user agents to bring things into the present day.  [issue](https://github.com/skoczen/django-seo-js/pull/41).

### 0.3.4 - Jan 8, 2020
Fixes googlebot defaults [issue](https://github.com/skoczen/django-seo-js/issues/39).

### 0.3.3 - Jan 8, 2020

Add `SEO_JS_SEND_USER_AGENT` setting.

### 0.3.2 - March 6, 2019

See [releases](https://github.com/skoczen/django-seo-js/releases)

### 0.3.1 - March 3, 2015

* **Deprecation**: `django_seo_js.middleware.HashBangMiddleware` is now called `django_seo_js.middleware.EscapedFragmentMiddleware`, to fix confusion.  `HashBangMiddleware` will be removed in 0.5.  Which I would bet is probably late 2015, early 2016.  You'll see a log warning from now on.  Thanks to [thoop](https://github.com/thoop) for the report.
* Bugfix to user agent middleware not respecting `ENABLED`, thanks to [rchrd2](https://github.com/rchrd2). Also reported by [denisvlr](https://github.com/denisvlr).
* New (backwards-compatible) `build_absolute_uri` method that can be overridden, thanks to [chazcb](https://github.com/chazcb).
* Removed Google, Yahoo, and Bing from the default `USER_AGENTS`, since they now support the escaped fragment protocol (and leaving them in can cause a cloaking penalty.)  Thanks to [thoop](https://github.com/thoop) for pointing this out.

### 0.3.0 - Feb 5, 2015

* Fixes to the `update_url` method, thanks to [denisvlr](https://github.com/denisvlr).
* Optimizations in lookups, thanks to [mattrobenolt](https://github.com/mattrobenolt).
* Changes behavior to more sanely not follow redirects, per [#9](https://github.com/skoczen/django-seo-js/issues/9), thanks to [denisvlr](https://github.com/denisvlr) and [mattrobenolt](https://github.com/mattrobenolt).

### 0.2.4 - August 12, 2014

* Adds a few more user agents to the defaults, per #7, and the suggestion of [andrewebdev](https://github.com/andrewebdev)

### 0.2.3 - May 28, 2014

* Adds an optional `SEO_JS_IGNORE_EXTENSIONS` setting that contains a list of extensions to ignore, thanks to the suggestion by [thoop](https://github.com/thoop).

### 0.2.2 - May 22, 2014

* Adds an optional `SEO_JS_IGNORE_URLS` setting, that contains a list of urls to ignore, thanks to the sitemap.xml prerender bug reported by [alex-mcleod](https://github.com/alex-mcleod).

### 0.2.1 - May 19, 2014

* **Backwards incompatible** changes to `SEOBackendBase` - all backends are now expected to return an `HttpResponse` for their `get_response_for_url` methods. If you have custom backends, they'll need to be updated.  All included backends have been updated, so if you're using an included backend, you can just pip install the new version, and go.
* Returns pages that come back from the cache with anything besides a `5xx` status code.
* Passes on headers, content type, and status code from the cache response.
* If the backend return a `5xx` status, just returns the normal app and hopes for the best.


### 0.1.3 - May 13, 2014

* Adds a `SEO_JS_ENABLED` setting, so you can disable hooks and middlewares during tests.


### 0.1.2 - May 9, 2014

* Handles cases where a request didn't come with a User-agent.


### 0.1.1 - May 9, 2014

* Improvements to unit tests.


### 0.1 - May 8, 2014

* Includes `PrerenderIO` and `PrerenderHosted` backends.
* First release - we're using this in production at [GreenKahuna ScrapBin](http://scrapbin.com).

