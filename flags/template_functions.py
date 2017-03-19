from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist

from wagtail.wagtailcore.models import Site

from flags.models import Flag


def flag_enabled(request, flag_name):
    """ Check if a flag is enabled for a given request """
    # Check for settings-defined flags first.
    settings_flags = getattr(settings, 'FLAGS', {})
    try:
        return settings_flags[flag_name]
    except KeyError:
        pass

    # Get the Wagtail site for this request
    site = Site.find_for_request(request)

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


def flags_enabled(request, *flag_names):
    """ Check if all flags are enabled for a given request """
    return all(flag_enabled(request, flag_name) for flag_name in flag_names)


def flag_disabled(request, flag_name):
    """ Check if a flag is disabled for a given request """
    return not flag_enabled(request, flag_name)
