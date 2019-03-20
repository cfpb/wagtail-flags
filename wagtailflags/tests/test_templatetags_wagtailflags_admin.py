from django.test import TestCase, override_settings

from flags.sources import get_flags

from wagtailflags.templatetags.wagtailflags_admin import (
    conditions, disablable, enablable, enabled, required_conditions, state_str
)


class TestWagtailFlagsAdminTemplateTags(TestCase):

    @override_settings(FLAGS={'MYFLAG': [('boolean', True)]})
    def test_enabled_enabled(self):
        flag = get_flags().get('MYFLAG')
        self.assertTrue(enabled(flag))

    @override_settings(FLAGS={'MYFLAG': [('boolean', False)]})
    def test_enabled_disabled(self):
        flag = get_flags().get('MYFLAG')
        self.assertFalse(enabled(flag))

    @override_settings(FLAGS={'MYFLAG': [('boolean', False)]})
    def test_enablable_disabled_not_required(self):
        flag = get_flags().get('MYFLAG')
        self.assertTrue(enablable(flag))

    @override_settings(FLAGS={'MYFLAG': [('boolean', True)]})
    def test_enablable_enabled_not_required(self):
        flag = get_flags().get('MYFLAG')
        self.assertFalse(enablable(flag))

    @override_settings(FLAGS={'MYFLAG': [('boolean', True, True)]})
    def test_enablable_disabled_required(self):
        flag = get_flags().get('MYFLAG')
        self.assertFalse(enablable(flag))

    @override_settings(FLAGS={'MYFLAG': [('boolean', True)]})
    def test_disablable_disabled_not_required(self):
        flag = get_flags().get('MYFLAG')
        self.assertTrue(disablable(flag))

    @override_settings(FLAGS={'MYFLAG': [('boolean', False)]})
    def test_disablable_enabled_not_required(self):
        flag = get_flags().get('MYFLAG')
        self.assertFalse(disablable(flag))

    @override_settings(FLAGS={'MYFLAG': [('boolean', False, True)]})
    def test_disablable_enabled_required(self):
        flag = get_flags().get('MYFLAG')
        self.assertFalse(disablable(flag))

    @override_settings(FLAGS={'MYFLAG': [
        ('boolean', True),
        ('path matches', '/mypath'),
    ]})
    def test_conditions(self):
        flag = get_flags().get('MYFLAG')
        self.assertEqual(len(conditions(flag)), 1)

    @override_settings(FLAGS={'MYFLAG': [
        ('path matches', '/mypath', True),
        ('path matches', '/myotherpath'),
    ]})
    def test_required_conditions(self):
        flag = get_flags().get('MYFLAG')
        self.assertEqual(len(required_conditions(flag)), 1)


class TestStateStrTemplateTag(TestCase):

    @override_settings(FLAGS={'MYFLAG': [
        ('anonymous', 'False', True),
    ]})
    def test_state_str_required_no_optional_no_bool(self):
        flag = get_flags().get('MYFLAG')
        self.assertEqual(
            'MYFLAG is <b>enabled</b> when <i>all</i> required conditions '
            'are met.',
            state_str(flag)
        )

    @override_settings(FLAGS={'MYFLAG': [
        ('anonymous', 'False', True),
        ('boolean', True),
    ]})
    def test_state_str_required_no_optional_bool_true(self):
        flag = get_flags().get('MYFLAG')
        self.assertEqual(
            'MYFLAG is <b>enabled</b> when <i>all</i> required conditions '
            'are met.',
            state_str(flag)
        )

    @override_settings(FLAGS={'MYFLAG': [
        ('anonymous', 'False', True),
        ('boolean', False),
    ]})
    def test_state_str_required_no_optional_bool_false(self):
        flag = get_flags().get('MYFLAG')
        self.assertEqual(
            'MYFLAG is <b>disabled</b> when <i>all</i> required conditions '
            'are met.',
            state_str(flag)
        )

    @override_settings(FLAGS={'MYFLAG': [
        ('anonymous', 'False', True),
        ('path matches', '/mypath'),
        ('boolean', False),
    ]})
    def test_state_str_required_optional_bool_false(self):
        flag = get_flags().get('MYFLAG')
        self.assertEqual(
            'MYFLAG is <b>enabled</b> when <i>all</i> required conditions '
            'and <i>any</i> optional condition is met.',
            state_str(flag)
        )

    @override_settings(FLAGS={'MYFLAG': [
        ('anonymous', 'False', True),
        ('boolean', True, True),
        ('path matches', '/mypath'),
    ]})
    def test_state_str_required_optional_bool_true_required(self):
        flag = get_flags().get('MYFLAG')
        self.assertEqual(
            'MYFLAG is <b>enabled</b> for all requests.',
            state_str(flag)
        )

    @override_settings(FLAGS={'MYFLAG': [
        ('anonymous', 'False', True),
        ('boolean', False, True),
        ('path matches', '/mypath'),
    ]})
    def test_state_str_required_optional_bool_false_required(self):
        flag = get_flags().get('MYFLAG')
        self.assertEqual(
            'MYFLAG is <b>disabled</b> for all requests.',
            state_str(flag)
        )

    @override_settings(FLAGS={'MYFLAG': [
        ('anonymous', 'False'),
        ('boolean', True),
    ]})
    def test_state_str_no_required_optional_bool_true(self):
        flag = get_flags().get('MYFLAG')
        self.assertEqual(
            'MYFLAG is <b>enabled</b> for all requests.',
            state_str(flag)
        )

    @override_settings(FLAGS={'MYFLAG': [
        ('anonymous', 'False', True),
        ('path matches', '/mypath'),
    ]})
    def test_state_str_required_optional_no_bool(self):
        flag = get_flags().get('MYFLAG')
        self.assertEqual(
            'MYFLAG is <b>enabled</b> when <i>all</i> required conditions '
            'and <i>any</i> optional condition is met.',
            state_str(flag)
        )

    @override_settings(FLAGS={'MYFLAG': [
        ('path matches', '/mypath'),
    ]})
    def test_state_str_non_bool_optional(self):
        flag = get_flags().get('MYFLAG')
        self.assertEqual(
            'MYFLAG is <b>enabled</b> when <i>any</i> optional condition '
            'is met.',
            state_str(flag)
        )

    @override_settings(FLAGS={'MYFLAG': [('boolean', False)]})
    def test_state_str_bool_false(self):
        flag = get_flags().get('MYFLAG')
        self.assertEqual(
            'MYFLAG is <b>disabled</b> for all requests.',
            state_str(flag)
        )

    @override_settings(FLAGS={'MYFLAG': [('boolean', True)]})
    def test_state_str_bool_true(self):
        flag = get_flags().get('MYFLAG')
        self.assertEqual(
            'MYFLAG is <b>enabled</b> for all requests.',
            state_str(flag)
        )
