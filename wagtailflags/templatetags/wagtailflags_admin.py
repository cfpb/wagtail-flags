from django import template

from flags.templatetags.flags_debug import bool_enabled


register = template.Library()


@register.filter
def enablable(flag):
    """Return true if a flag is enablable by Wagtail-Flags.
    A flag is enablable by Wagtail-Flags if it has a required boolean
    condition and that boolean condition is False."""
    return not any(
        c.required for c in flag.conditions if c.condition == "boolean"
    ) and not bool_enabled(flag)


@register.filter
def disablable(flag):
    """Return true if a flag is disabable by Wagtail-Flags.
    A flag is disablable by Wagtail-Flags if it has a required boolean
    condition and that boolean condition is True."""
    return not any(
        c.required for c in flag.conditions if c.condition == "boolean"
    ) and bool_enabled(flag)


@register.filter
def deletable(flag):
    """Return true if a flag is deletable by Wagtail-Flags.
    A flag is deletable by Wagtal-Flags if it is database-only, which means it
    will have a non-None "obj" attribute."""
    return not any(
        c for c in flag.conditions if getattr(c, "obj", None) is None
    )
