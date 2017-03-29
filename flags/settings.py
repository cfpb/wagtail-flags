import logging

from django.conf import settings
from django.utils.module_loading import import_string

logger = logging.getLogger(__name__)

# Private set of all global flags from sources in FLAG_SOURCES. This is
# populated on AppConfig.ready() by add_flags_from_sources below.
SOURCED_FLAGS = {}


def add_flags_from_sources(sources=None):
    """ Read flags from sources defined in settings.FLAG_SOURCES.
    FLAG_SOURCES is expected to be a list of Python module with flags
    specified with variable assignment, e.g. MY_FLAG = True """
    global SOURCED_FLAGS

    if sources is None:
        sources = getattr(settings, 'FLAG_SOURCES', ())

    for source_str in sources:
        source = import_string(source_str)
        for flag in (f for f in dir(source)
                     if f.isupper() and isinstance(getattr(source, f), bool)):
            SOURCED_FLAGS[flag] = getattr(source, flag)


def get_global_flags(sourced_flags=None):
    """ Get all global flags and their state.
    This combines FLAGS from settings with all possible FLAG_SOURCES. """
    global_flags = getattr(settings, 'FLAGS', {})
    if sourced_flags is None:
        sourced_flags = SOURCED_FLAGS

    # Global flags override everything. If there is a flag in a module defined
    # in settings.FLAG_SOURCES and a flag defined in settings.FLAGS,
    # settings.FLAGS wins.
    for flag, value in sourced_flags.items():
        global_flags.setdefault(flag, value)

    return global_flags
