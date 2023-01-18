from unittest import mock

from django.test import TestCase

from wagtail.test.utils import WagtailTestUtils

from flags.models import FlagState

from wagtailflags.signals import flag_disabled, flag_enabled


class SignalsTestCase(TestCase, WagtailTestUtils):
    def setUp(self):
        self.login()

        self.dbonly_flag = FlagState.objects.create(
            name="DBONLY_FLAG",
            condition="boolean",
            value="True",
            required=False,
        )

    def test_flag_enabled_was_sent(self):
        mock_handler = mock.Mock()
        flag_enabled.connect(mock_handler)
        self.client.get("/admin/flags/FLAG_DISABLED/", {"enable": ""})
        mock_handler.assert_called_with(
            sender=mock.ANY, flag_name="FLAG_DISABLED", signal=mock.ANY
        )

    def test_flag_disabled_was_sent(self):
        mock_handler = mock.Mock()
        flag_disabled.connect(mock_handler)
        self.client.get("/admin/flags/DBONLY_FLAG/", {"disable": ""})
        mock_handler.assert_called_with(
            sender=mock.ANY, flag_name="DBONLY_FLAG", signal=mock.ANY
        )
