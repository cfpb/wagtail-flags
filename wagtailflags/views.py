from collections import OrderedDict

from django.shortcuts import get_object_or_404, redirect, render

from flags.forms import FlagStateForm
from flags.models import FlagState
from flags.settings import get_flags


def index(request):
    flags = OrderedDict(sorted(get_flags().items(), key=lambda x: x[0]))
    context = {
        'flag_states': FlagState.objects.order_by('name'),
        'flags': flags,
    }
    return render(request, 'wagtailflags/index.html', context)


def create(request):
    if request.method == 'POST':
        form = FlagStateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('wagtailflags:list')
    else:
        form = FlagStateForm()

    context = dict(form=form)
    return render(request, 'wagtailflags/flags/create.html', context)


def delete(request, state_id):
    flag_state = get_object_or_404(FlagState, pk=state_id)

    if request.method == 'POST':
        flag_state.delete()
        return redirect('wagtailflags:list')

    context = dict(state_str=str(flag_state), state_id=flag_state.pk)
    return render(request, 'wagtailflags/flags/delete.html', context)
