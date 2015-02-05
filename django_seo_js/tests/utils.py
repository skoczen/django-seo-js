from functools import wraps
from django_seo_js import settings


class override_settings(object):
    def __init__(self, **kwargs):
        self.options = kwargs
        self.originals = {}

    def __enter__(self):
        self.enable()

    def __exit__(self, exc_type, exc_value, traceback):
        self.disable()

    def __call__(self, test_func):
        @wraps(test_func)
        def inner(*args, **kwargs):
            with self:
                return test_func(*args, **kwargs)
        return inner

    def enable(self):
        for k, v in self.options.items():
            self.originals[k] = getattr(settings, k)
            setattr(settings, k, v)

    def disable(self):
        for k, v in self.originals.items():
            setattr(settings, k, v)
