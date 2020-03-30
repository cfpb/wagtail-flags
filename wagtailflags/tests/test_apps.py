from django.test import TestCase

from flags.conditions import get_conditions


class TestWagtailFlagsApps(TestCase):
    def test_condition_registration(self):
        self.assertIn("site", get_conditions())
