from django import forms

from flags.conditions import get_conditions
from flags.models import FlagState
from flags.sources import get_flags


class NewFlagForm(forms.ModelForm):
    name = forms.CharField(label="Name", required=True)

    def clean_name(self):
        name = self.cleaned_data["name"]
        if name in get_flags():
            raise forms.ValidationError(
                "Flag named {} already exists".format(name)
            )
        return name

    def save(self, commit=True):
        obj = super(NewFlagForm, self).save(commit=False)
        obj.condition = "boolean"
        obj.value = "False"
        obj.required = False
        obj.save()
        return obj

    class Meta:
        model = FlagState
        fields = ("name",)


class FlagStateForm(forms.ModelForm):
    name = forms.CharField(
        label="Flag", required=True, disabled=True, widget=forms.HiddenInput(),
    )
    condition = forms.ChoiceField(label="Condition", required=True)
    value = forms.CharField(label="Expected value", required=True)
    required = forms.BooleanField(
        label="Required",
        required=False,
        help_text=(
            'All conditions marked "required" must be met to enable '
            "the flag"
        ),
    )

    def __init__(self, *args, **kwargs):
        super(FlagStateForm, self).__init__(*args, **kwargs)

        self.fields["condition"].choices = [
            (c, c) for c in sorted(get_conditions()) if c != "boolean"
        ]

    class Meta:
        model = FlagState
        fields = ("name", "condition", "value", "required")
