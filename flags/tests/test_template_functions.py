from django.http import HttpRequest
from django.test import TestCase

from wagtail.wagtailcore.models import Site

from flags.models import Flag
from flags.template_functions import flag_disabled, flag_enabled


class TemplateFunctionsTestCase(TestCase):
    def setUp(self):
        self.site = Site.objects.get(is_default_site=True)
        self.request = HttpRequest()
        self.request.site = self.site

    def test_flag_enabled_true(self):
        Flag.objects.create(key='TEST_FLAG', enabled_by_default=True)
        self.assertTrue(flag_enabled('TEST_FLAG', self.request))

    def test_flag_enabled_false(self):
        Flag.objects.create(key='TEST_FLAG', enabled_by_default=False)
        self.assertFalse(flag_enabled('TEST_FLAG', self.request))

    def test_flag_disabled_true(self):
        Flag.objects.create(key='TEST_FLAG', enabled_by_default=False)
        self.assertTrue(flag_disabled('TEST_FLAG', self.request))

    def test_flag_disabled_false(self):
        Flag.objects.create(key='TEST_FLAG', enabled_by_default=True)
        self.assertFalse(flag_disabled('TEST_FLAG', self.request))
