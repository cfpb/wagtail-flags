from django.http import HttpRequest
from django.template import Context, Template
from django.test import TestCase

from wagtail.wagtailcore.models import Site

from flags.models import Flag


class FlagsTemplateTagsTestCase(TestCase):

    def setUp(self):
        self.flag_names = ('ONE', 'TWO', 'THREE')
        self.site = Site.objects.get(is_default_site=True)
        self.request = HttpRequest()
        self.request.site = self.site

    def render_template(self, string, context=None):
        context = context or {'request': self.request}
        context = Context(context)
        return Template(string).render(context)

    def test_flag_enabled_disabled(self):
        rendered = self.render_template(
            '{% load feature_flags %}'
            '{% flag_enabled "TEMPLATETAG_TEST"  as test_flag %}'
            '{% if test_flag %}'
            'flag enabled'
            '{% else %}'
            'flag disabled'
            '{% endif %}'
        )
        self.assertEqual(rendered, 'flag disabled')

    def test_flag_enabled_enabled(self):
        Flag.objects.create(key='TEMPLATETAG_TEST', enabled_by_default=True)
        rendered = self.render_template(
            '{% load feature_flags %}'
            '{% flag_enabled "TEMPLATETAG_TEST"  as test_flag %}'
            '{% if test_flag %}'
            'flag enabled'
            '{% else %}'
            'flag disabled'
            '{% endif %}'
        )
        self.assertEqual(rendered, 'flag enabled')

    def test_flag_disabled_disabled(self):
        # Disabled can also mean non-existent
        rendered = self.render_template(
            '{% load feature_flags %}'
            '{% flag_disabled "TEMPLATETAG_TEST"  as test_flag %}'
            '{% if test_flag %}'
            'flag disabled'
            '{% else %}'
            'flag enabled'
            '{% endif %}'
        )
        self.assertEqual(rendered, 'flag disabled')

    def test_flag_disabled_enabled(self):
        Flag.objects.create(key='TEMPLATETAG_TEST', enabled_by_default=True)
        rendered = self.render_template(
            '{% load feature_flags %}'
            '{% flag_disabled "TEMPLATETAG_TEST"  as test_flag %}'
            '{% if test_flag %}'
            'flag disabled'
            '{% else %}'
            'flag enabled'
            '{% endif %}'
        )
        self.assertEqual(rendered, 'flag enabled')
