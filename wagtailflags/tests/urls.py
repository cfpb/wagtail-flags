from django.conf.urls import include, url


try:  # pragma: no cover; Wagtail >= 2.0
    from wagtail.admin import urls as wagtailadmin_urls
except ImportError:  # pragma: no cover; fallback for Wagtail < 2.0
    from wagtail.wagtailadmin import urls as wagtailadmin_urls


urlpatterns = [
    url(r'^admin/', include(wagtailadmin_urls)),
]
