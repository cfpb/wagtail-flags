from django.test import RequestFactory, TestCase

import wagtail

from flags.conditions import RequiredForCondition

from wagtailflags.conditions import site_condition


if wagtail.VERSION > (3, 0, 0):  # pragma: no cover
    from wagtail.models import Site
else:  # pragma: no cover
    from wagtail.core.models import Site


class SiteConditionTestCase(TestCase):
    def setUp(self):
        self.site = Site.objects.get(is_default_site=True)
        self.factory = RequestFactory()
        self.request = self.factory.get("/")
        Site.find_for_request(self.request)

    def test_site_valid_string(self):
        self.assertTrue(site_condition("localhost:80", request=self.request))

    def test_site_valid_string_no_port(self):
        self.assertTrue(site_condition("localhost", request=self.request))

    def test_site_valid_string_default_port(self):
        self.assertTrue(
            site_condition("localhost [default]", request=self.request)
        )

    def test_site_valid_site(self):
        self.assertTrue(site_condition(str(self.site), request=self.request))

    def test_site_invalid_site(self):
        self.assertFalse(
            site_condition("non.existent.site", request=self.request)
        )

    def test_request_required(self):
        with self.assertRaises(RequiredForCondition):
            site_condition("localhost:80")
