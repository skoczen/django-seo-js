from django.test import TestCase
from django.template import Template, Context


class TagsTest(TestCase):

    def test_seo_js_head(self):
        t = Template("{% load django_seo_js %}{% seo_js_head %}")
        c = Context({})
        rendered_html = t.render(c)
        self.assertEqual(rendered_html, """<meta name="fragment" content="!">""")