from wagtail.admin import urls as wagtailadmin_urls


try:  # pragma: no cover; >= 2.0
    from django.urls import include, re_path
except ImportError:  # pragma: no cover; fallback for Django < 2.0
    from django.conf.urls import include, url as re_path


urlpatterns = [
    re_path(r"^admin/", include(wagtailadmin_urls)),
]
