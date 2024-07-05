from django.templatetags.static import static
from django.urls import include, path, reverse
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
        path("", views.index, name="list"),
        path("create/", views.create_flag, name="create_flag"),
        path("<name>/", views.flag_index, name="flag_index"),
        path(
            "<name>/delete/",
            views.delete_flag,
            name="delete_flag",
        ),
        path(
            "<name>/create/",
            views.edit_condition,
            name="create_condition",
        ),
        path(
            "<name>/<int:condition_pk>/",
            views.edit_condition,
            name="edit_condition",
        ),
        path(
            "<name>/<int:condition_pk>/delete/",
            views.delete_condition,
            name="delete_condition",
        ),
    ]

    urlpatterns = [
        path(
            "flags/",
            include((flagpatterns, "wagtailflags"), namespace="wagtailflags"),
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
