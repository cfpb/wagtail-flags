import django
from django.templatetags.static import static
from django.urls import include, re_path, reverse
from django.utils.html import format_html

from wagtail import hooks
from wagtail.admin.menu import MenuItem

from wagtailflags import views


@hooks.register("register_settings_menu_item")
def register_flags_menu():
    return MenuItem(
        "Flags",
        reverse("wagtailflags:list"),
        icon_name="flag",
        order=10000,
    )


@hooks.register("register_admin_urls")
def register_flag_admin_urls():
    flagpatterns = [
        re_path(r"^$", views.index, name="list"),
        re_path(r"^create/$", views.create_flag, name="create_flag"),
        re_path(r"^(?P<name>[\w\-]+)/$", views.flag_index, name="flag_index"),
        re_path(
            r"^(?P<name>[\w\-]+)/delete/$",
            views.delete_flag,
            name="delete_flag",
        ),
        re_path(
            r"^(?P<name>[\w\-]+)/create/$",
            views.edit_condition,
            name="create_condition",
        ),
        re_path(
            r"^(?P<name>[\w\-]+)/(?P<condition_pk>\d+)/$",
            views.edit_condition,
            name="edit_condition",
        ),
        re_path(
            r"^(?P<name>[\w\-]+)/(?P<condition_pk>\d+)/delete/$",
            views.delete_condition,
            name="delete_condition",
        ),
    ]

    if django.VERSION >= (1, 10):  # pragma: no cover
        urlpatterns = [
            re_path(
                r"^flags/",
                include(
                    (flagpatterns, "wagtailflags"), namespace="wagtailflags"
                ),
            )
        ]
    else:  # pragma: no cover; fallback for Django < 1.10
        urlpatterns = [
            re_path(
                r"^flags/",
                include((flagpatterns, "wagtailflags", "wagtailflags")),
            )
        ]

    return urlpatterns


@hooks.register("insert_global_admin_css", order=100)
def global_admin_css():
    return format_html(
        '<link rel="stylesheet" href="{}">',
        static("wagtailflags/css/wagtailflags.css"),
    )


@hooks.register("register_icons")
def register_icons(icons):
    return icons + ["wagtailflags/flag.svg"]
