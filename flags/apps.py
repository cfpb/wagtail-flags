from django.apps import AppConfig
from django.db.models.signals import post_migrate

from flags.settings import add_flags_from_sources


def post_migrate_flags_app(app_config, **kwargs):
    """ Dynamic conditions are not available to used for flags until after
    our models are fully migrated. """
    app_config.dynamic_conditions_ready = True


class WagtailFlagsConfig(AppConfig):
    name = 'flags'
    verbose_name = 'Wagtail Flags'
    dynamic_conditions_ready = False

    def ready(self):
        add_flags_from_sources()
        post_migrate.connect(post_migrate_flags_app, sender=self)
