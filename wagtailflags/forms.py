from django import forms

from flags.forms import FlagStateForm as DjangoFlagsFlagStateForm
from flags.models import FlagState
from flags.sources import get_flags


class NewFlagForm(forms.ModelForm):
    name = forms.SlugField(label="Name", required=True)

    def clean_name(self):
        name = self.cleaned_data["name"]
        if name in get_flags():
            raise forms.ValidationError(f"Flag named {name} already exists")
        return name

    def save(self, commit=True):
        obj = super().save(commit=False)
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        condition_field = self.fields.get("condition")
        if condition_field is None:
            return

        editing_boolean = (
            self.instance is not None
            and self.instance.pk is not None
            and self.instance.condition == "boolean"
        )
        if not editing_boolean:
            condition_field.widget.choices = [
                choice
                for choice in condition_field.choices
                if choice[0] != "boolean"
            ]

    def clean_condition(self):
        condition = self.cleaned_data["condition"]

        editing_boolean = (
            self.instance is not None
            and self.instance.pk is not None
            and self.instance.condition == "boolean"
        )
        if condition == "boolean" and not editing_boolean:
            raise forms.ValidationError(
                "Boolean conditions are managed by the enable/disable button."
            )

        return condition

    def clean_value(self):
        if self.cleaned_data.get("condition") is None:
            return self.cleaned_data.get("value")

        return super().clean_value()

    class Meta:
        model = FlagState
        fields = ("name", "condition", "value", "required")
