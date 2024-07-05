from django.test import TestCase

from wagtail.test.utils import WagtailTestUtils

from flags.models import FlagState


class TestWagtailFlagsViews(TestCase, WagtailTestUtils):
    def setUp(self):
        self.login()

        self.dbonly_flag = FlagState.objects.create(
            name="DBONLY_FLAG",
            condition="boolean",
            value="True",
            required=False,
        )

    def test_flags_index(self):
        response = self.client.get("/admin/flags/")
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, "FLAG_ENABLED")
        self.assertContains(response, "FLAG_DISABLED")
        self.assertContains(response, "DBONLY_FLAG")
        self.assertContains(response, "<b>enabled</b> when")
        self.assertContains(response, "<b>enabled</b> for")

    def test_flag_create(self):
        response = self.client.get("/admin/flags/create/")
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            "/admin/flags/create/", {"name": "NEW_FLAG"}
        )
        self.assertRedirects(response, "/admin/flags/NEW_FLAG/")
        self.assertEqual(FlagState.objects.count(), 2)
        new_flag_condition = FlagState.objects.get(name="NEW_FLAG")
        self.assertEqual(new_flag_condition.condition, "boolean")
        self.assertEqual(new_flag_condition.value, "False")
        self.assertEqual(new_flag_condition.required, False)

    def test_flag_create_existing(self):
        response = self.client.get("/admin/flags/create/")
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            "/admin/flags/create/", {"name": "DBONLY_FLAG"}
        )
        self.assertContains(response, "Flag named DBONLY_FLAG already exists")

    def test_flag_delete(self):
        response = self.client.get("/admin/flags/DBONLY_FLAG/delete/")
        self.assertEqual(response.status_code, 200)

        response = self.client.post("/admin/flags/DBONLY_FLAG/delete/")

        self.assertRedirects(response, "/admin/flags/")
        self.assertEqual(FlagState.objects.count(), 0)

    def test_flag_delete_nonexistent(self):
        response = self.client.get(
            "/admin/flags/THIS_FLAG_DOES_NOT_EXIST/delete/"
        )
        self.assertEqual(response.status_code, 404)

    def test_flag_delete_not_deletable(self):
        response = self.client.get("/admin/flags/FLAG_ENABLED/delete/")
        self.assertEqual(response.status_code, 403)

    def test_flag_index_nonexistent_flag_raises_404(self):
        response = self.client.get("/admin/flags/THIS_FLAG_DOES_NOT_EXIST/")
        self.assertEqual(response.status_code, 404)

    def test_flag_index(self):
        response = self.client.get("/admin/flags/FLAG_DISABLED/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "FLAG_DISABLED")
        self.assertContains(response, "path matches")
        self.assertContains(response, "Enable FLAG_DISABLED")

    def test_flag_index_enabled(self):
        response = self.client.get("/admin/flags/FLAG_ENABLED/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Disable FLAG_ENABLED")

    def test_flag_index_disabled(self):
        response = self.client.get("/admin/flags/FLAG_DISABLED/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Enable FLAG_DISABLED")

    def test_flag_index_enabled_required_true(self):
        response = self.client.get("/admin/flags/FLAG_ENABLED/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Disable FLAG_ENABLED")

    def test_flag_index_disabled_required_true(self):
        response = self.client.get("/admin/flags/FLAG_ENABLED/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Disable FLAG_ENABLED")

    def test_enable_flag(self):
        condition_query = FlagState.objects.filter(name="FLAG_DISABLED")
        self.assertEqual(len(condition_query.all()), 0)

        response = self.client.get(
            "/admin/flags/FLAG_DISABLED/", {"enable": ""}
        )
        self.assertRedirects(response, "/admin/flags/FLAG_DISABLED/")
        self.assertEqual(len(condition_query.all()), 1)
        self.assertEqual(condition_query.first().condition, "boolean")
        self.assertEqual(condition_query.first().value, "True")

    def test_enable_flag_with_required_true(self):
        condition_query = FlagState.objects.filter(name="FLAG_DISABLED")
        self.assertEqual(len(condition_query.all()), 0)

        self.client.get("/admin/flags/FLAG_DISABLED/", {"enable": ""})
        self.assertEqual(len(condition_query.all()), 1)
        self.assertEqual(condition_query.first().condition, "boolean")
        self.assertEqual(condition_query.first().value, "True")

    def test_disable_flag(self):
        condition_query = FlagState.objects.filter(name="DBONLY_FLAG")
        self.client.get("/admin/flags/DBONLY_FLAG/", {"disable": ""})
        self.assertEqual(len(condition_query.all()), 1)
        self.assertEqual(condition_query.first().condition, "boolean")
        self.assertEqual(condition_query.first().value, "False")

    def test_disable_flag_with_required_true(self):
        condition_query = FlagState.objects.filter(name="DBONLY_FLAG")
        self.client.get("/admin/flags/DBONLY_FLAG/", {"disable": ""})
        self.assertEqual(len(condition_query.all()), 1)
        self.assertEqual(condition_query.first().condition, "boolean")
        self.assertEqual(condition_query.first().value, "False")

    def test_create_flag_condition_nonexistent_flag_raises_404(self):
        response = self.client.get(
            "/admin/flags/THIS_FLAG_DOES_NOT_EXIST/create/"
        )
        self.assertEqual(response.status_code, 404)

    def test_create_flag_condition(self):
        response = self.client.get("/admin/flags/DBONLY_FLAG/create/")
        self.assertEqual(response.status_code, 200)

        params = {
            "condition": "path matches",
            "value": "/db_path",
        }
        response = self.client.post("/admin/flags/DBONLY_FLAG/create/", params)
        self.assertRedirects(response, "/admin/flags/DBONLY_FLAG/")
        self.assertEqual(len(FlagState.objects.all()), 2)

    def test_edit_flag_condition_nonexistent_flag_raises_404(self):
        response = self.client.get("/admin/flags/THIS_FLAG_DOES_NOT_EXIST/99/")
        self.assertEqual(response.status_code, 404)

    def test_edit_flag_condition(self):
        condition_obj = FlagState.objects.create(
            name="DBONLY_FLAG", condition="boolean", value="true"
        )
        response = self.client.get(
            f"/admin/flags/DBONLY_FLAG/{condition_obj.pk}/"
        )
        self.assertEqual(response.status_code, 200)

        params = {
            "condition": "boolean",
            "value": "true",
        }

        response = self.client.post(
            f"/admin/flags/DBONLY_FLAG/{condition_obj.pk}/", params
        )
        self.assertRedirects(response, "/admin/flags/DBONLY_FLAG/")
        self.assertEqual(
            FlagState.objects.get(pk=condition_obj.pk).value, "true"
        )

    def test_delete_flag_condition_nonexistent_flag_raises_404(self):
        response = self.client.get(
            "/admin/flags/THIS_FLAG_DOES_NOT_EXIST/99/delete/"
        )
        self.assertEqual(response.status_code, 404)

    def test_delete_flag_condition(self):
        condition_obj = FlagState.objects.create(
            name="DBONLY_FLAG", condition="boolean", value="true"
        )
        self.assertEqual(len(FlagState.objects.all()), 2)
        response = self.client.get(
            f"/admin/flags/DBONLY_FLAG/{condition_obj.pk}/delete/"
        )
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            f"/admin/flags/DBONLY_FLAG/{condition_obj.pk}/delete/"
        )
        self.assertRedirects(response, "/admin/flags/DBONLY_FLAG/")
        self.assertEqual(len(FlagState.objects.all()), 1)
