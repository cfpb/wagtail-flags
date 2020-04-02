from django import template

from flags.templatetags.flags_debug import bool_enabled


register = template.Library()


@register.filter
def enablable(flag):
    return not any(
        c.required for c in flag.conditions if c.condition == "boolean"
    ) and not bool_enabled(flag)


@register.filter
def disablable(flag):
    return not any(
        c.required for c in flag.conditions if c.condition == "boolean"
    ) and bool_enabled(flag)
