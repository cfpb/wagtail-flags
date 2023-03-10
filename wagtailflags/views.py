from django.http import Http404, HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render

from flags.models import FlagState
from flags.sources import get_flags
from flags.templatetags.flags_debug import bool_enabled

from wagtailflags.forms import FlagStateForm, NewFlagForm
from wagtailflags.signals import flag_disabled, flag_enabled
from wagtailflags.templatetags.wagtailflags_admin import deletable


def index(request):
    context = {
        "flags": sorted(get_flags().values(), key=lambda x: x.name),
    }
    return render(request, "wagtailflags/index.html", context)


def create_flag(request):
    """Create a new flag.
    This will add a FlagState object with a custom name and a boolean: False
    condition"""
    if request.method == "POST":
        form = NewFlagForm(
            request.POST,
            initial={
                "condition": "path matches",
                "value": "/foo",
                "required": False,
            },
        )
        if form.is_valid():
            form.save()
            return redirect("wagtailflags:flag_index", name=form.instance.name)
    else:
        form = NewFlagForm()

    context = dict(form=form)
    return render(request, "wagtailflags/flags/create_flag.html", context)


def delete_flag(request, name):
    """Delete a database flag."""
    flag = get_flags().get(name)

    if not flag:
        raise Http404

    if not deletable(flag):
        return HttpResponseForbidden(name)

    if request.method == "POST":
        FlagState.objects.filter(name=name).delete()
        return redirect("wagtailflags:list")

    context = {
        "flag": flag,
    }
    return render(request, "wagtailflags/flags/delete_flag.html", context)


def flag_index(request, name):
    flag = get_flags().get(name)

    if not flag:
        raise Http404

    # If there's a database boolean condition, fetch it and treat it as a
    # on/off switch
    if "enable" in request.GET or "disable" in request.GET:
        db_boolean_condition = next(
            (
                c
                for c in flag.conditions
                if c.condition == "boolean"
                and getattr(c, "obj", None) is not None
            ),
            None,
        )

        if db_boolean_condition is None:
            boolean_condition_obj = FlagState.objects.create(
                name=name, condition="boolean", value="True"
            )
        else:
            boolean_condition_obj = db_boolean_condition.obj

        if "enable" in request.GET and not bool_enabled(flag):
            boolean_condition_obj.value = True
            flag_enabled.send(sender=flag_index, flag_name=flag.name)
        elif "disable" in request.GET and bool_enabled(flag):
            boolean_condition_obj.value = False
            flag_disabled.send(sender=flag_index, flag_name=flag.name)

        boolean_condition_obj.save()
        return redirect("wagtailflags:flag_index", name=name)

    context = {
        "flag": flag,
    }
    return render(request, "wagtailflags/flags/flag_index.html", context)


def edit_condition(request, name, condition_pk=None):
    flag = get_flags().get(name)

    if not flag:
        raise Http404

    try:
        condition = FlagState.objects.get(pk=condition_pk)
        title_str = f"Edit {condition} condition"
    except FlagState.DoesNotExist:
        condition = None
        title_str = f"Create a condition on {flag.name}"

    if request.method == "POST":
        form = FlagStateForm(
            request.POST, initial={"name": name}, instance=condition
        )
        if form.is_valid():
            form.save()
            return redirect("wagtailflags:flag_index", name=name)

    else:
        form = FlagStateForm(initial={"name": name}, instance=condition)

    context = {
        "flag": flag,
        "form": form,
        "condition_str": str(condition),
        "condition_pk": condition_pk,
        "title": title_str,
    }
    return render(request, "wagtailflags/flags/edit_condition.html", context)


def delete_condition(request, name, condition_pk):
    flag = get_flags().get(name)

    if not flag:
        raise Http404

    condition = get_object_or_404(FlagState, pk=condition_pk)

    if request.method == "POST":
        condition.delete()
        return redirect("wagtailflags:flag_index", name=name)

    context = {
        "flag": flag,
        "condition_str": str(condition),
        "condition_pk": condition.pk,
    }
    return render(request, "wagtailflags/flags/delete_condition.html", context)
