import os

import wagtail

ALLOWED_HOSTS = ["*"]

SECRET_KEY = "not needed"

ROOT_URLCONF = "wagtailflags.tests.urls"

DATABASES = {
    "default": {
        "ENGINE": os.environ.get(
            "DATABASE_ENGINE", "django.db.backends.sqlite3"
        ),
        "NAME": os.environ.get("DATABASE_NAME", "wagtailflags.db"),
        "USER": os.environ.get("DATABASE_USER", None),
        "PASSWORD": os.environ.get("DATABASE_PASS", None),
        "HOST": os.environ.get("DATABASE_HOST", None),
        "TEST": {"NAME": os.environ.get("DATABASE_NAME", None)},
    },
}

INSTALLED_APPS = (
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
)

WAGTAIL_APPS = (
    "wagtail.contrib.forms",
    "wagtail.contrib.modeladmin",
    "wagtail.contrib.settings",
    "wagtail.admin",
    "wagtail.documents",
    "wagtail.images",
    "wagtail.sites",
    "wagtail.users",
)

WAGTAILADMIN_RICH_TEXT_EDITORS = {
    "default": {"WIDGET": "wagtail.admin.rich_text.DraftailRichTextArea"},
}

# Wagtail 3.0 moves testapp from wagtail.tests to wagtail.test
if wagtail.VERSION >= (3, 0, 0):  # pragma: no cover
    WAGTAIL_APPS += (
        "wagtail",
        "wagtail.test.testapp",
    )
    WAGTAILADMIN_RICH_TEXT_EDITORS["custom"] = {
        "WIDGET": "wagtail.test.testapp.rich_text.CustomRichTextArea"
    }
else:  # pragma: no cover
    WAGTAIL_APPS += (
        "wagtail.core",
        "wagtail.tests.testapp",
    )
    WAGTAILADMIN_RICH_TEXT_EDITORS["custom"] = {
        "WIDGET": "wagtail.tests.testapp.rich_text.CustomRichTextArea"
    }

MIDDLEWARE = (
    "django.middleware.common.CommonMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
)

INSTALLED_APPS = (
    (
        "django.contrib.admin",
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.messages",
        "django.contrib.sessions",
        "django.contrib.staticfiles",
        "taggit",
    )
    + WAGTAIL_APPS
    + (
        "flags",
        "wagtailflags",
    )
)

STATIC_ROOT = "/tmp/static/"
STATIC_URL = "/static/"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.request",
            ],
            "debug": True,
        },
    },
]

WAGTAIL_SITE_NAME = "Test Site"

FLAGS = {
    "FLAG_ENABLED": [{"condition": "boolean", "value": True}],
    "FLAG_DISABLED": [
        {"condition": "path matches", "value": "/disabled_path"}
    ],
}
