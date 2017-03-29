from django.apps import AppConfig

from flags.settings import add_flags_from_sources

# Private set of all global flags from sources in FLAG_SOURCES.
# Possible importable sources of global flags. This is expected to be a list
# of Python module with flags specified with variable assignment, e.g.
# MY_FLAG = True
__SOURCED_FLAGS = {}


class WagtailFlagsConfig(AppConfig):
    name = 'flags'
    verbose_name = 'Wagtail Flags'

    def ready(self):
        add_flags_from_sources()
