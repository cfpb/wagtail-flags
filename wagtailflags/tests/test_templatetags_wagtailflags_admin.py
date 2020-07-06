from django.test import TestCase, override_settings

from flags.sources import get_flags

from wagtailflags.templatetags.wagtailflags_admin import disablable, enablable


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
