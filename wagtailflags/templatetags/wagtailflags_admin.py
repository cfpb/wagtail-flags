from django import template

from flags.sources import DatabaseCondition
from flags.templatetags.flags_debug import bool_enabled


register = template.Library()


@register.filter
def enablable(flag):
    """Return true if a flag is enablable by Wagtail-Flags.

    A flag is enablable by Wagtail-Flags if it has a required boolean
    condition and that boolean condition is False.
    """
    return not any(
        c.required for c in flag.conditions if c.condition == "boolean"
    ) and not bool_enabled(flag)


@register.filter
def disablable(flag):
    """Return true if a flag is disablable by Wagtail-Flags.

    A flag is disablable by Wagtail-Flags if it has a required boolean
    condition and that boolean condition is True.
    """
    return not any(
        c.required for c in flag.conditions if c.condition == "boolean"
    ) and bool_enabled(flag)


@register.filter
def deletable(flag):
    """Return true if a flag is deletable by Wagtail-Flags.

    A flag is deletable by Wagtail-Flags if it is database-only, which means
    all of its conditions are type DatabaseCondition.
    """
    return flag.conditions and all(
        isinstance(c, DatabaseCondition) for c in flag.conditions
    )
