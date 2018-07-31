import django
from django.conf.urls import include, url

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
        url(r'^(\d+)/delete/$', views.delete,
            name='delete'),
        url(r'^create/$', views.create, name='create'),
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
