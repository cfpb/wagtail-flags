from django.apps import AppConfig


class WagtailFlagsAppConfig(AppConfig):
    name = "wagtailflags"
    verbose_name = "Wagtail Flags"

    def ready(self):
        # Import custom conditions to ensure that they get registered.
        import wagtailflags.conditions  # noqa
