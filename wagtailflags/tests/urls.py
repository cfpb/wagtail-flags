from django.urls import include, re_path

from wagtail.admin import urls as wagtailadmin_urls


urlpatterns = [
    re_path(r"^admin/", include(wagtailadmin_urls)),
]
