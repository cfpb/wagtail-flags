from django.http import HttpRequest
from django.test import TestCase

from flags.conditions import RequiredForCondition
from wagtailflags.conditions import site_condition


try:
    from wagtail.core.models import Site
except ImportError:  # pragma: no cover; fallback for Wagtail < 2.0
    from wagtail.wagtailcore.models import Site


class SiteConditionTestCase(TestCase):

    def setUp(self):
        self.site = Site.objects.get(is_default_site=True)
        self.request = HttpRequest()
        self.request.site = self.site

    def test_site_valid_string(self):
        self.assertTrue(site_condition('localhost:80', request=self.request))

    def test_site_valid_string_no_port(self):
        self.assertTrue(site_condition('localhost', request=self.request))

    def test_site_valid_string_default_port(self):
        self.assertTrue(site_condition('localhost [default]',
                                       request=self.request))

    def test_site_valid_site(self):
        self.assertTrue(site_condition(str(self.site), request=self.request))

    def test_site_invalid_site(self):
        self.assertFalse(site_condition('non.existent.site',
                                        request=self.request))

    def test_request_required(self):
        with self.assertRaises(RequiredForCondition):
            site_condition('localhost:80')
