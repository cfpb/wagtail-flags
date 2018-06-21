from __future__ import absolute_import, unicode_literals

import os

import django

import wagtail


ALLOWED_HOSTS = ['*']

SECRET_KEY = 'not needed'

ROOT_URLCONF = 'wagtailflags.tests.urls'

DATABASES = {
    'default': {
        'ENGINE': os.environ.get(
            'DATABASE_ENGINE',
            'django.db.backends.sqlite3'
        ),
        'NAME': os.environ.get('DATABASE_NAME', 'wagtailflags'),
        'USER': os.environ.get('DATABASE_USER', None),
        'PASSWORD': os.environ.get('DATABASE_PASS', None),
        'HOST': os.environ.get('DATABASE_HOST', None),

        'TEST': {
            'NAME': os.environ.get('DATABASE_NAME', None),
        },
    },
}

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
)

if wagtail.VERSION >= (2, 0):  # pragma: no cover
    WAGTAIL_APPS = (
        'wagtail.contrib.forms',
        'wagtail.contrib.modeladmin',
        'wagtail.contrib.settings',
        'wagtail.tests.testapp',
        'wagtail.admin',
        'wagtail.core',
        'wagtail.documents',
        'wagtail.images',
        'wagtail.sites',
        'wagtail.users',
    )

    WAGTAIL_MIDDLEWARE = (
        'wagtail.core.middleware.SiteMiddleware',
    )

    WAGTAILADMIN_RICH_TEXT_EDITORS = {
        'default': {
            'WIDGET': 'wagtail.admin.rich_text.DraftailRichTextArea'
        },
        'custom': {
            'WIDGET': 'wagtail.tests.testapp.rich_text.CustomRichTextArea'
        },
    }
else:  # pragma: no cover; fallback for Wagtail < 2.0
    WAGTAIL_APPS = (
        'wagtail.contrib.modeladmin',
        'wagtail.contrib.settings',
        'wagtail.tests.testapp',
        'wagtail.wagtailadmin',
        'wagtail.wagtailcore',
        'wagtail.wagtaildocs',
        'wagtail.wagtailforms',
        'wagtail.wagtailimages',
        'wagtail.wagtailsites',
        'wagtail.wagtailusers',
    )

    WAGTAIL_MIDDLEWARE = (
        'wagtail.wagtailcore.middleware.SiteMiddleware',
    )

    WAGTAILADMIN_RICH_TEXT_EDITORS = {
        'default': {
            'WIDGET': 'wagtail.wagtailadmin.rich_text.HalloRichTextArea',
        },
        'custom': {
            'WIDGET': 'wagtail.tests.testapp.rich_text.CustomRichTextArea'
        },
    }

if django.VERSION >= (1, 10):  # pragma: no cover
    MIDDLEWARE = (
        'django.middleware.common.CommonMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ) + WAGTAIL_MIDDLEWARE
else:  # pragma: no cover; fallback for Django >= 1.10
    MIDDLEWARE_CLASSES = (
        'django.middleware.common.CommonMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ) + WAGTAIL_MIDDLEWARE

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
    'taggit',
) + WAGTAIL_APPS + (
    'flags',
    'wagtailflags',
)

STATIC_URL = '/static/'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.request',
            ],
            'debug': True,
        },
    },
]

WAGTAIL_SITE_NAME = 'Test Site'

FLAGS = {
    'FLAG_ENABLED': {'boolean': True},
    'FLAG_DISABLED': {},
    'DB_FLAG': {},
}
