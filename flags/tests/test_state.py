from django.http import HttpRequest
from django.test import TestCase, override_settings

from wagtail.wagtailcore.models import Site

from flags.models import Flag, FlagState
from flags.state import (
    flag_state,
    flag_enabled,
    flag_disabled
)


@override_settings(
    FLAGS={
        'GLOBAL_FLAG_ENABLED': True,
        'GLOBAL_FLAG_ENABLED2': True,
        'GLOBAL_FLAG_DISABLED': False,
    }
)
class FlagStateTestCase(TestCase):
    def setUp(self):
        self.site = Site.objects.get(is_default_site=True)
        self.request = HttpRequest()
        self.request.site = self.site

    def test_non_existent_flag(self):
        """ Non-existent flags always have a default state of False """
        self.assertFalse(flag_state('FLAG_DOES_NOT_EXIST'))

    def test_flag_state_global_enabled(self):
        """ Global flags that are enabled should be True """
        self.assertTrue(flag_state('GLOBAL_FLAG_ENABLED'))

    def test_flag_state_global_disabled(self):
        """ Global flags that are disabled should be False """
        self.assertFalse(flag_state('GLOBAL_FLAG_DISABLED'))

    def test_flag_state_global_disabled_enabled_db(self):
        """ Disabled Global flags override enabled Site flags """
        flag = Flag.objects.create(key='GLOBAL_FLAG_DISABLED')
        FlagState.objects.create(flag=flag, site=self.site, enabled=True)
        self.assertFalse(flag_state('GLOBAL_FLAG_DISABLED', self.site))

    def test_flag_state_global_enabled_enabled_db(self):
        """ Enabled Global flags override disabled Site flags """
        flag = Flag.objects.create(key='GLOBAL_FLAG_ENABLED')
        FlagState.objects.create(flag=flag, site=self.site, enabled=False)
        self.assertTrue(flag_state('GLOBAL_FLAG_ENABLED', self.site))

    def test_flag_state_non_existent_flag_site(self):
        """ Given a site non-existent flags should still be False """
        # This ensures that all the try/except fall-throughs work
        self.assertFalse(flag_state('FLAG_DOES_NOT_EXIST', self.site))

    def test_flag_state_site_default_false(self):
        """ A site flag that's disabled by default should be False """
        Flag.objects.create(key='SITE_FLAG', enabled_by_default=False)
        self.assertFalse(flag_state('SITE_FLAG', self.site))

    def test_flag_state_site_default_true(self):
        """ A site flag that that's enabled by default should be True """
        Flag.objects.create(key='SITE_FLAG', enabled_by_default=True)
        self.assertTrue(flag_state('SITE_FLAG', self.site))

    def test_flag_state_site_false(self):
        """ A site flag disabled for a site should be False """
        flag = Flag.objects.create(key='SITE_FLAG')
        FlagState.objects.create(flag=flag, site=self.site, enabled=False)
        self.assertFalse(flag_state('SITE_FLAG', self.site))

    def test_flag_state_site_true(self):
        """ A site flag enabled for a site should be True """
        flag = Flag.objects.create(key='SITE_FLAG')
        FlagState.objects.create(flag=flag, site=self.site, enabled=True)
        self.assertTrue(flag_state('SITE_FLAG', self.site))

    def test_flag_state_site_for_other_site(self):
        """ A site flag enabled for an other site should be False """
        flag = Flag.objects.create(key='SITE_FLAG')
        other_site = Site.objects.create(
            is_default_site=False,
            root_page_id=self.site.root_page_id
        )
        FlagState.objects.create(flag=flag, site=other_site, enabled=True)
        self.assertFalse(flag_state('SITE_FLAG', self.site))

    def test_flag_state_request(self):
        """ flag_state() should find a Site in an HttpRequest """
        flag = Flag.objects.create(key='SITE_FLAG')
        FlagState.objects.create(flag=flag, site=self.site, enabled=True)
        self.assertTrue(flag_state('SITE_FLAG', self.request))

    def test_flag_enabled_global_enabled(self):
        """ Global flags enabled should be True """
        self.assertTrue(flag_enabled('GLOBAL_FLAG_ENABLED'))

    def test_flag_enabled_global_disabled(self):
        """ Global flags disabled should be False """
        self.assertFalse(flag_enabled('GLOBAL_FLAG_DISABLED'))

    def test_flag_enabled_site_enabled(self):
        """ flag_enabled should pass the Site as expected """
        flag = Flag.objects.create(key='SITE_FLAG')
        FlagState.objects.create(flag=flag, site=self.site, enabled=True)
        self.assertTrue(flag_enabled('SITE_FLAG', self.site))

    def test_flag_enabled_site_enabled_request(self):
        """ flag_enabled should pass the HttpRequest as expected """
        flag = Flag.objects.create(key='SITE_FLAG')
        FlagState.objects.create(flag=flag, site=self.site, enabled=True)
        self.assertTrue(flag_enabled('SITE_FLAG', self.request))

    def test_flag_disabled_global_disabled(self):
        """ Global flags disabled should be True """
        self.assertTrue(flag_disabled('GLOBAL_FLAG_DISABLED'))

    def test_flag_disabled_global_enabled(self):
        """ Global flags enabled should be False """
        self.assertFalse(flag_disabled('GLOBAL_FLAG_ENABLED'))

    def test_flag_disabled_site_enabled(self):
        """ flag_disabled should pass the Site as expected """
        flag = Flag.objects.create(key='SITE_FLAG')
        FlagState.objects.create(flag=flag, site=self.site, enabled=False)
        self.assertTrue(flag_disabled('SITE_FLAG', self.site))

    def test_flag_disabled_request_enabled(self):
        """ flag_disabled should pass the HttpRequest as expected """
        flag = Flag.objects.create(key='SITE_FLAG')
        FlagState.objects.create(flag=flag, site=self.site, enabled=True)
        self.assertFalse(flag_disabled('SITE_FLAG', self.request))
