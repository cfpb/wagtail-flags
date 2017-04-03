from django.core.exceptions import ObjectDoesNotExist

from wagtail.wagtailcore.models import Site

from flags.models import Flag
from flags.settings import get_global_flags


def flag_state(flag_name, request_or_site=None):
    """ Return the value for the flag.
    If request_or_site is a request or Site object, the flag state is checked
    for a Wagtail site, otherwise only global flags are checked. """

    # Check for global flags first.
    settings_flags = get_global_flags()
    if flag_name in settings_flags:
        return settings_flags[flag_name]

    # Get the Wagtail site for this request
    try:
        site = Site.find_for_request(request_or_site)
    except AttributeError:
        # Is it Site-like?
        if hasattr(request_or_site, 'flag_states'):
            site = request_or_site
        else:
            # We can't do anything with this
            return False

    # See if we have a flag that is enabled for this site
    try:
        return site.flag_states.get(flag_id=flag_name).enabled
    except ObjectDoesNotExist:
        pass

    # If not, then see if the flag exists at all and is perhaps enabled
    # by default
    try:
        return Flag.objects.get(key=flag_name).enabled_by_default
    except ObjectDoesNotExist:
        return False


def flag_enabled(flag_name, request_or_site=None):
    """ Check if a flag is enabled.
    If request_or_site is a request or Site object, the flag state is checked
    for a Wagtail site, otherwise only global flags are checked. """
    return flag_state(flag_name, request_or_site=request_or_site)


def flag_disabled(flag_name, request_or_site=None):
    """ Check if a flag is disabled.
    If request_or_site is a request or Site object, the flag state is checked
    for a Wagtail site, otherwise only global flags are checked. """
    return not flag_state(flag_name, request_or_site=request_or_site)
