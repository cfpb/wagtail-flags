from django import forms

from flags.forms import FlagStateForm as DjangoFlagsFlagStateForm
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


class FlagStateForm(DjangoFlagsFlagStateForm):
    name = forms.CharField(
        label="Flag",
        required=True,
        disabled=True,
        widget=forms.HiddenInput(),
    )

    class Meta:
        model = FlagState
        fields = ("name", "condition", "value", "required")
