# Wagtail-Flags

[![Build Status](https://travis-ci.org/cfpb/wagtail-flags.svg?branch=master)](https://travis-ci.org/cfpb/wagtail-flags)
[![Coverage Status](https://coveralls.io/repos/github/cfpb/wagtail-flags/badge.svg?branch=master)](https://coveralls.io/github/cfpb/wagtail-flags?branch=master)

Feature flags allow you to toggle functionality in the Wagtail based on configurable conditions. 

Wagtail-Flags adds a Wagtail admin UI and Wagtail Site-based condition on top of [Django-Flags](https://github.com/cfpb/django-flags). For a more complete overview of feature flags and how to use them, please see the [Django-Flags documentation](https://cfpb.github.io/django-flags).

![Feature flags in the Wagtail admin](https://raw.githubusercontent.com/cfpb/wagtail-flags/master/screenshot_list.png)

- [Dependencies](#dependencies)
- [Installation](#installation)
- [Usage](#usage)
- [Extended conditions](#built-in-conditions)
- [Getting help](#getting-help)
- [Getting involved](#getting-involved)
- [Licensing](#licensing)
- [Credits and references](#credits-and-references)

## Dependencies

- Django 1.8+ (including Django 2.0)
- Wagtail 1.10+ (including Wagtail 2.0)
- Django-Flags 3.0+ 
- Python 2.7+, 3.6+

## Installation

1. Install wagtail-flags:

```shell
pip install wagtail-flags
```

2. Add `flags` and `wagtailflags` as installed apps in your Django `settings.py`:

 ```python
 INSTALLED_APPS = (
     ...
     'flags',
     'wagtailflags',
     ...
 )
```

## Usage

Please see the [Django-Flags documentation](https://cfpb.github.io/django-flags) for the most current information about defining and checking feature flags.

First, define the flag in Django `settings.py`:

```python
FLAGS = {
    'MY_FLAG': {}
}
```

Then use the flag in a Django template (`mytemplate.html`):

```django
{% load feature_flags %}
{% flag_enabled 'MY_FLAG' as my_flag %}

{% if my_flag %}
  <div class="flagged-banner">
    I’m the result of a feature flag.   
  </div>
{% endif %}
```

Next, configure a URL for that template (`urls.py`):

```python
from django.urls import path
from django.views.generic import TemplateView

urlpatterns = [
    path(r'mypage/', TemplateView.as_view(template_name='mytemplate.html')),
]
```

Finally, add conditions for the flag in the Wagtail admin under "Settings", "Flags":

![Creating conditions in the Wagtail admin](https://raw.githubusercontent.com/cfpb/wagtail-flags/master/screenshot_create.png)

## Extended conditions

Wagtail-Flags adds the following conditions to Django-Flags:

##### `site`

Allows a flag to be enabled for a Wagtail site that matches the hostname and port in the condition value.

```python
FLAGS = {'MY_FLAG': {'site': 'staging.mysite.com'}}
```

## Getting help

Please add issues to the [issue tracker](https://github.com/cfpb/wagtail-flags/issues).

## Getting involved

General instructions on _how_ to contribute can be found in [CONTRIBUTING](CONTRIBUTING.md).

## Licensing
1. [TERMS](TERMS.md)
2. [LICENSE](LICENSE)
3. [CFPB Source Code Policy](https://github.com/cfpb/source-code-policy/)

## Credits and references

1. Forked from [cfgov-refresh](https://github.com/cfpb/cfgov-refresh)
