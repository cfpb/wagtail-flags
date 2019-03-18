from django.test import TestCase

from wagtail.tests.utils import WagtailTestUtils

from flags.models import FlagState
from flags.sources import get_flags

from wagtailflags.templatetags.wagtailflags import enabled, conditions


class TestWagtailFlagsTemplateTags(TestCase, WagtailTestUtils):

    def setUp(self):
        self.login()

    def test_enabled_enabled(self):
        FlagState.objects.create(
            name='MYFLAG',
            condition='boolean',
            value='True'
        )
        flag = get_flags().get('MYFLAG')
        self.assertTrue(enabled(flag))

    def test_enabled_disabled(self):
        FlagState.objects.create(
            name='MYFLAG',
            condition='boolean',
            value='False'
        )
        flag = get_flags().get('MYFLAG')
        self.assertTrue(enabled(flag))

    def test_conditions(self):
        # Boolean conditions should be treated seperate from all others
        FlagState.objects.create(
            name='MYFLAG',
            condition='boolean',
            value='True'
        )
        FlagState.objects.create(
            name='MYFLAG',
            condition='path matches',
            value='/mypath'
        )
        flag = get_flags().get('MYFLAG')
        self.assertEqual(len(conditions(flag)), 1)
