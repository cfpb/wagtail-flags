from django.test import TestCase

from wagtail.tests.utils import WagtailTestUtils

from flags.models import FlagState


class TestWagtailFlagsViews(TestCase, WagtailTestUtils):

    def setUp(self):
        self.login()

    def test_flags_index(self):
        self.orphaned_flag = FlagState.objects.create(
            name='ORPHANED_FLAG',
            condition='boolean',
            value='True'
        )

        response = self.client.get('/admin/flags/')
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, 'FLAG_ENABLED')
        self.assertContains(response, 'is enabled when')

        self.assertContains(response, 'FLAG_DISABLED')
        self.assertContains(response, 'is never enabled')

        self.assertIn(
            self.orphaned_flag,
            response.context['flag_states']
        )
        self.assertNotIn(
            self.orphaned_flag.name,
            response.context['flags']
        )

    def test_flags_delete(self):
        state_obj = FlagState.objects.create(
            name='',
            condition='boolean',
            value='True'
        )
        self.assertEqual(len(FlagState.objects.all()), 1)
        response = self.client.get(
            '/admin/flags/' + str(state_obj.pk) + '/delete/'
        )
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            '/admin/flags/' + str(state_obj.pk) + '/delete/'
        )
        self.assertRedirects(response, '/admin/flags/')
        self.assertEqual(len(FlagState.objects.all()), 0)

    def test_flags_create(self):
        response = self.client.get('/admin/flags/create/')
        self.assertEqual(response.status_code, 200)

        params = {
            'name': 'DB_FLAG',
            'condition': 'boolean',
            'value': 'True',
        }
        response = self.client.post('/admin/flags/create/', params)
        self.assertRedirects(response, '/admin/flags/')
        self.assertEqual(len(FlagState.objects.all()), 1)
