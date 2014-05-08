from django import template
register = template.Library()


@register.simple_tag
def seo_js_head(*args):
    return """<meta name="fragment" content="!">"""
