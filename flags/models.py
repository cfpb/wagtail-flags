from django.db import models

from wagtail.wagtailadmin.edit_handlers import FieldPanel, MultiFieldPanel
from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.url_routing import RouteResult

from flags.edit_handlers import FlagChooserPanel
from flags.state import flag_enabled


class FlagState(models.Model):
    """ Flag state conditions can either be hardcoded in settings or stored in
    the database. This model stores the conditions in the database. """
    name = models.CharField(max_length=64)
    condition = models.CharField(max_length=64, default='boolean')
    value = models.CharField(max_length=127, default='True')

    class Meta:
        app_label = 'flags'
        unique_together = ('name', 'condition', 'value')

    def __str__(self):
        return "{name} is enabled when {condition} is {value}".format(
            name=self.name, condition=self.condition, value=self.value)


class FlaggablePageMixin(models.Model):
    """ This is a model mixin class can be be mixed-in along side the Wagtail
    Page model (or a subclass thereof) to add the viewing of the latest draft
    revision instead of the published revision based on feature flag state.
    It is an alternative to inheriting directly from FlaggablePage. """

    feature_flag_name = models.CharField(
        verbose_name="Feature flag",
        max_length=64,
        blank=True,
        help_text=("The selected feature flag will control whether the draft "
                   "version of this page is visible live for the feature "
                   "flag's conditions")
    )
    show_draft_with_feature_flag = models.BooleanField(
        verbose_name="Show draft",
        default=False,
        help_text=("Show the latest draft of this page live regardless of "
                   "published status, when the selected feature flag is "
                   "enabled.")
    )

    flag_panels = [
        FieldPanel('show_draft_with_feature_flag', 'Feature flag enabled'),
        FlagChooserPanel('feature_flag_name'),
    ]

    settings_panels = [
        MultiFieldPanel(flag_panels, 'Feature flagged drafts'),
    ]

    class Meta:
        abstract = True

    def serve_flaggable(self, request, *args, **kwargs):
        latest_revision = self.get_latest_revision_as_page()
        if (flag_enabled(latest_revision.feature_flag_name, request=request)
                and latest_revision.show_draft_with_feature_flag):
            return Page.serve(latest_revision, request, *args, **kwargs)

        return Page.serve(self, request, *args, **kwargs)

    def route_flaggable(self, request, path_components):
        if path_components:
            return Page.route(self, request, path_components)
        else:
            latest_revision = self.get_latest_revision_as_page()
            if (flag_enabled(latest_revision.feature_flag_name,
                             request=request)
                    and latest_revision.show_draft_with_feature_flag):
                return RouteResult(self)
            else:
                return Page.route(self, request, path_components)


class FlaggablePage(Page, FlaggablePageMixin):
    """ This Page class can be inheritted by a Wagtail Page model and allow
    the viewing of the latest draft revision instead of the published revision
    based on feature flag state. """

    # This page can't be created directly, only subclasses of it
    is_creatable = False

    def serve(self, request, *args, **kwargs):
        return self.serve_flaggable(request, *args, **kwargs)

    def route(self, request, path_components):
        return self.route_flaggable(request, path_components)
