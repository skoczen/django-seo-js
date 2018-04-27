from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag
def seo_js_head(*args):
    return mark_safe("""<meta name="fragment" content="!">""")
