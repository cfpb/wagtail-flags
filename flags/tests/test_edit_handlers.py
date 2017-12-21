from django import forms
from django.test import TestCase, override_settings

from wagtail.wagtailadmin.edit_handlers import ObjectList

from flags.edit_handlers import FlagChooserPanel
from flags.models import FlaggablePage


@override_settings(FLAGS={'TEST_FLAG': {}})
class TestFlagChooserPanel(TestCase):

    def setUp(self):
        self.EditHandler = ObjectList([
            FlagChooserPanel('feature_flag_name')
        ]).bind_to_model(FlaggablePage)
        self.FlagChooserPanel = self.EditHandler.children[0]

        self.FlaggablePageForm = self.EditHandler.get_form_class(FlaggablePage)

        self.page = FlaggablePage(
            title='Test flagged page',
            feature_flag_name='TEST_FLAG'
        )

        self.form = self.FlaggablePageForm(instance=self.page)

    def test_flag_chooser_uses_correct_widget(self):
        self.assertEqual(
            type(self.form.fields['feature_flag_name'].widget),
            forms.Select
        )

    def test_render_as_object(self):
        field_panel = self.FlagChooserPanel(
            instance=self.page,
            form=self.form
        )
        result = field_panel.render_as_object()

        self.assertIn('<legend>Feature flag</legend>', result)
        self.assertNotIn(
            '<label for="id_feature_flag_name">Feature flag:</label>',
            result)

        # check that the populated form field is included
        self.assertIn('value="TEST_FLAG"', result)

        # there should be no errors on this field
        self.assertNotIn('<p class="error-message">', result)

    def test_render_as_field(self):
        form = self.FlaggablePageForm(
            {'title': 'Test flagged page'},
            instance=self.page
        )
        form.is_valid()

        field_panel = self.FlagChooserPanel(
            instance=self.page,
            form=form
        )
        result = field_panel.render_as_field()

        # check that label is output in the 'field' style
        self.assertIn(
            '<label for="id_feature_flag_name">Feature flag:</label>',
            result)
        self.assertNotIn('<legend>Feature flag</legend>', result)

        # check that the populated form field is included
        self.assertIn('value="TEST_FLAG"', result)

        # there should be no errors on this field
        self.assertNotIn('<p class="error-message">', result)
