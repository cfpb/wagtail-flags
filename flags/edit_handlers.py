from django import forms

from wagtail.wagtailadmin.edit_handlers import BaseFieldPanel

from flags.settings import get_flags


class BaseFlagChooserPanel(BaseFieldPanel):
    @classmethod
    def widget_overrides(cls):
        flag_choices = [('', '')] + [(k, k) for k in get_flags().keys()]
        return {cls.field_name: forms.Select(choices=flag_choices)}


class FlagChooserPanel(object):

    def __init__(self, field_name):
        self.field_name = field_name

    def bind_to_model(self, model):
        return type(str('_FlagChoserPanel'), (BaseFlagChooserPanel,), {
            'model': model,
            'field_name': self.field_name,
        })
