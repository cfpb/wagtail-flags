from django.test import TestCase, override_settings

from flags.models import FlagState
from flags.sources import get_flags

from wagtailflags.templatetags.wagtailflags_admin import (
    deletable,
    disablable,
    enablable,
)


class TestWagtailFlagsAdminTemplateTags(TestCase):
    @override_settings(FLAGS={"MYFLAG": [("boolean", False)]})
    def test_enablable_disabled_not_required(self):
        flag = get_flags().get("MYFLAG")
        self.assertTrue(enablable(flag))

    @override_settings(FLAGS={"MYFLAG": [("boolean", True)]})
    def test_enablable_enabled_not_required(self):
        flag = get_flags().get("MYFLAG")
        self.assertFalse(enablable(flag))

    @override_settings(FLAGS={"MYFLAG": [("boolean", True, True)]})
    def test_enablable_disabled_required(self):
        flag = get_flags().get("MYFLAG")
        self.assertFalse(enablable(flag))

    @override_settings(FLAGS={"MYFLAG": [("boolean", True)]})
    def test_disablable_disabled_not_required(self):
        flag = get_flags().get("MYFLAG")
        self.assertTrue(disablable(flag))

    @override_settings(FLAGS={"MYFLAG": [("boolean", False)]})
    def test_disablable_enabled_not_required(self):
        flag = get_flags().get("MYFLAG")
        self.assertFalse(disablable(flag))

    @override_settings(FLAGS={"MYFLAG": [("boolean", False, True)]})
    def test_disablable_enabled_required(self):
        flag = get_flags().get("MYFLAG")
        self.assertFalse(disablable(flag))

    @override_settings(FLAGS={"MYFLAG": [("boolean", False)], "EMPTYFLAG": []})
    def test_deletable(self):
        FlagState.objects.create(
            name="DBFLAG",
            condition="boolean",
            value="True",
        )
        self.assertFalse(deletable(get_flags().get("MYFLAG")))
        self.assertFalse(deletable(get_flags().get("EMPTYFLAG")))
        self.assertTrue(deletable(get_flags().get("DBFLAG")))
