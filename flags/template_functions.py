from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist

from wagtail.wagtailcore.models import Site

from flags.models import Flag


def flag_enabled(request, flag_name):
    site = Site.find_for_request(request)

    try:
        return site.flag_states.get(flag_id=flag_name).enabled
    except ObjectDoesNotExist:
        pass

    try:
        return Flag.objects.get(key=flag_name).enabled_by_default
    except ObjectDoesNotExist:
        return False


def flags_enabled(request, *flag_names):


def flag_disabled(request, flag_name):
