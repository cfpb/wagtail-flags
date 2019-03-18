from django import template


register = template.Library()


@register.filter
def enabled(flag):
    return any(c.value for c in flag.conditions if c.condition == 'boolean')


@register.filter
def conditions(flag):
    return [c for c in flag.conditions if c.condition != 'boolean']
