from django.apps import apps
from django.core.exceptions import ObjectDoesNotExist

from flags.conditions import RequiredForCondition, register


@register('site')
def site_condition(site_str, request=None, **kwargs):
    """ Does the requests's Wagtail Site match the given site?
    site_str should be 'hostname:port', or 'hostname [default]'. """
    if request is None:
        raise RequiredForCondition("request is required for condition "
                                   "'site'")

    Site = apps.get_model('wagtailcore.Site')

    if '[default]' in site_str:
        # Wagtail Sites on the default port have [default] at the end of
        # their str() form.
        site_str = site_str.replace(' [default]', ':80')
    elif ':' not in site_str:
        # Add a default port if one isn't given
        site_str += ':80'

    hostname, port = site_str.split(':')
    try:
        conditional_site = Site.objects.get(hostname=hostname, port=port)
    except ObjectDoesNotExist:
        return False

    site = Site.find_for_request(request)

    return conditional_site == site
