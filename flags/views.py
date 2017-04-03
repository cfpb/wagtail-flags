from django.core.exceptions import ImproperlyConfigured
from django.forms import modelformset_factory
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect, render
from django.views.generic import TemplateView

from wagtail.wagtailcore.models import Site

from flags.decorators import flag_check
from flags.forms import FeatureFlagForm, FlagStateForm, SelectSiteForm
from flags.models import Flag, FlagState
from flags.utils import init_missing_flag_states_for_site
from flags.settings import get_global_flags


def select_site(request):
    if request.method == 'POST':
        form = SelectSiteForm(request.POST)

        if form.is_valid():
            site_id = form.cleaned_data['site_id']
            return redirect('flagadmin:list', site_id)
    else:
        default_site = Site.objects.all().filter(is_default_site=True).get()
        return redirect('flagadmin:list', (default_site.id),)


def create(request):
    if request.method == 'POST':
        form = FeatureFlagForm(request.POST)
        if form.is_valid():
            flag = Flag(key=form.cleaned_data['key'])
            flag.save()
            return redirect('flagadmin:select_site')
    else:
        form = FeatureFlagForm()

    context = dict(form=form)
    return render(request, 'flagadmin/flags/create.html', context)


def index(request, site_id):
    settings_flags = get_global_flags()

    sites = Site.objects.all()
    selected_site = Site.objects.get(pk=site_id)

    init_missing_flag_states_for_site(selected_site)
    FlagStateFormSet = modelformset_factory(
        FlagState,
        form=FlagStateForm,
        extra=0
    )

    flagstate_forms = FlagStateFormSet(
        queryset=selected_site.flag_states.all()
    )

    context = {
        'selected_site': selected_site,
        'sites': sites,
        'flagforms': flagstate_forms,
        'settings_flags': settings_flags,
    }

    return render(request, 'flagadmin/index.html', context)


def save(request, site_id):
    if request.method == 'POST':
        selected_site = Site.objects.get(pk=site_id)
        FlagStateFormSet = modelformset_factory(
            FlagState,
            form=FlagStateForm,
            extra=0
        )

        formset = FlagStateFormSet(request.POST)
        if formset.is_valid():
            formset.save()

        # this doesn't address what happens if the formset is invalid
        # index+save should probably be refactored as a single CBV
        return redirect('flagadmin:list', (selected_site.id),)


def delete(request, flag_id):
    flag = get_object_or_404(Flag, pk=flag_id)

    if request.method == 'POST':
        flag.delete()
        return redirect('flagadmin:select_site')

    context = dict(flag_id=flag.key)
    return render(request, 'flagadmin/flags/delete.html', context)


class FlaggedViewMixin(object):
    flag_name = None
    fallback = None
    condition = True

    def dispatch(self, request, *args, **kwargs):
        if self.flag_name is None:
            raise ImproperlyConfigured(
                "FlaggedViewMixin requires a 'flag_name' argument."
            )

        super_dispatch = super(FlaggedViewMixin, self).dispatch

        decorator = flag_check(
            self.flag_name,
            self.condition,
            fallback=self.fallback,
        )

        return decorator(super_dispatch)(request, *args, **kwargs)


class FlaggedTemplateView(FlaggedViewMixin, TemplateView):
    pass
