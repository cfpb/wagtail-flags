from django.test import TestCase, override_settings

from flags.settings import (
    SOURCED_FLAGS,
    add_flags_from_sources,
    get_global_flags
)

# Test flag for using this module to test
SOURCED_FLAG_ENABLED = True


class SettingsTestCase(TestCase):

    def test_add_flags_from_sources(self):
        add_flags_from_sources(sources=['flags.tests.test_settings'])
        self.assertTrue(SOURCED_FLAGS['SOURCED_FLAG_ENABLED'])

    def test_add_flags_from_sources_non_existent(self):
        with self.assertRaises(ImportError):
            add_flags_from_sources(sources=['non.existent.module'])

    @override_settings(FLAGS={'GLOBAL_FLAG_ENABLED': True})
    def test_get_global_flags(self):
        add_flags_from_sources(sources=['flags.tests.test_settings'])
        self.assertTrue(get_global_flags()['GLOBAL_FLAG_ENABLED'])
        self.assertTrue(get_global_flags()['SOURCED_FLAG_ENABLED'])

    @override_settings(FLAGS={'SOURCED_FLAG_ENABLED': False})
    def test_get_global_flags_global_overrides_sourced(self):
        add_flags_from_sources(sources=['flags.tests.test_settings'])
        self.assertFalse(get_global_flags()['SOURCED_FLAG_ENABLED'])
