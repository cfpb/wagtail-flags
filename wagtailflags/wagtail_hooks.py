import django
from django.conf.urls import include, url
from django.templatetags.static import static
from django.utils.html import format_html

from wagtailflags import views


try:  # pragma: no cover; >= 2.0
    from django.urls import reverse
except ImportError:  # pragma: no cover; fallback for Django < 2.0
    from django.core.urlresolvers import reverse

try:  # pragma: no cover; Wagtail >= 2.0
    from wagtail.admin.menu import MenuItem
    from wagtail.core import hooks
except ImportError:  # pragma: no cover; fallback for Wagtail < 2.0
    from wagtail.wagtailadmin.menu import MenuItem
    from wagtail.wagtailcore import hooks


@hooks.register('register_settings_menu_item')
def register_flags_menu():
    return MenuItem('Flags', reverse('wagtailflags:list'),
                    classnames='icon icon-tag', order=10000)


@hooks.register('register_admin_urls')
def register_flag_admin_urls():
    flagpatterns = [
        url(r'^$', views.index, name='list'),
        url(r'^create/$', views.create_flag, name='create_flag'),
        url(r'^(?P<name>[\w\-]+)/$', views.flag_index, name='flag_index'),
        url(
            r'^(?P<name>[\w\-]+)/create/$',
            views.edit_condition,
            name='create_condition'
        ),
        url(
            r'^(?P<name>[\w\-]+)/(?P<condition_pk>\d+)/$',
            views.edit_condition,
            name='edit_condition'
        ),
        url(
            r'^(?P<name>[\w\-]+)/(?P<condition_pk>\d+)/delete/$',
            views.delete_condition,
            name='delete_condition'
        ),
    ]

    if django.VERSION >= (1, 10):  # pragma: no cover
        urlpatterns = [
            url(r'^flags/',
                include((flagpatterns, 'wagtailflags'),
                        namespace='wagtailflags'))
        ]
    else:  # pragma: no cover; fallback for Django < 1.10
        urlpatterns = [
            url(r'^flags/',
                include((flagpatterns, 'wagtailflags', 'wagtailflags')))
        ]

    return urlpatterns


@hooks.register("insert_global_admin_css", order=100)
def global_admin_css():
    return format_html(
        '<link rel="stylesheet" href="{}">',
        static('wagtailflags/css/wagtailflags.css')
    )
