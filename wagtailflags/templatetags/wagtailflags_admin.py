from django import template
from django.utils.safestring import mark_safe


register = template.Library()


@register.filter
def enabled(flag):
    return any(c.check() for c in flag.conditions if c.condition == 'boolean')


@register.filter
def enablable(flag):
    return (
        not any(
            c.required for c in flag.conditions if c.condition == 'boolean'
        )
        and not enabled(flag)
    )


@register.filter
def disablable(flag):
    return (
        not any(
            c.required for c in flag.conditions if c.condition == 'boolean'
        )
        and enabled(flag)
    )


@register.filter
def conditions(flag):
    return [c for c in flag.conditions if c.condition != 'boolean']


@register.filter
def required_conditions(flag):
    return [c for c in conditions(flag) if c.required]


@register.filter
def state_str(flag):
    """ Construct a string that describes the current state of the flag """
    non_bool_conditions = conditions(flag)
    req_conditions = required_conditions(flag)
    bool_conditions = [c for c in flag.conditions if c.condition == 'boolean']
    req_bool_conditions = [c for c in bool_conditions if c.required]

    is_enabled = enabled(flag)

    state_str = flag.name + ' is'

    if len(req_bool_conditions) > 0:
        if is_enabled:
            state_str += ' <b>enabled</b> for all requests'
        else:
            state_str += ' <b>disabled</b> for all requests'

    elif len(non_bool_conditions) > 0:
        if len(req_conditions) > 0:
            state_str += ' <b>'

            if (len(bool_conditions) > 0 and
                    len(non_bool_conditions) == len(req_conditions) and
                    not is_enabled):
                state_str += 'disabled'
            else:
                state_str += 'enabled'

            state_str += '</b>'
            state_str += ' when <i>all</i> required conditions'

            if len(non_bool_conditions) == len(req_conditions):
                state_str += ' are met'

        elif is_enabled:
            state_str += ' <b>enabled</b> for all requests'
        else:
            state_str += ' <b>enabled</b> when'

        if not is_enabled:
            if len(non_bool_conditions) > len(req_conditions):
                if len(req_conditions) > 0:
                    state_str += ' and'
                state_str += ' <i>any</i> optional condition is met'

    elif is_enabled:
        state_str += ' <b>enabled</b> for all requests'
    else:
        state_str += ' <b>disabled</b> for all requests'

    state_str += '.'

    return mark_safe(state_str)
