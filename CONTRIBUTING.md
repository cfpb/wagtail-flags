# Guidance on how to contribute

> All contributions to this project will be released under the CC0 public domain
> dedication. By submitting a pull request or filing a bug, issue, or
> feature request, you are agreeing to comply with this waiver of copyright interest.
> Details can be found in our [TERMS](TERMS.md) and [LICENCE](LICENSE).

There are two primary ways to help:

- Using the issue tracker, and
- Changing the code-base.

## Using the issue tracker

Use the issue tracker to suggest feature requests, report bugs, and ask questions.
This is also a great way to connect with the developers of the project as well
as others who are interested in this solution.

Use the issue tracker to find ways to contribute. Find a bug or a feature, mention in
the issue that you will take on that effort, then follow the _Changing the code-base_
guidance below.

## Changing the code-base

Generally speaking, you should fork this repository, make changes in your
own fork, and then submit a pull-request. All new code should have associated unit
tests that validate implemented features and the presence or lack of defects.
Additionally, the code should follow any stylistic and architectural guidelines
prescribed by the project. In the absence of such guidelines, mimic the styles
and patterns in the existing code-base.

## Style

This project uses [`black`](https://github.com/psf/black) to format code,
[`isort`](https://github.com/timothycrosley/isort) to format imports,
and [`flake8`](https://gitlab.com/pycqa/flake8).

You can format code and imports by calling:

```
black wagtailflags
isort --recursive wagtailflags
```

And you can check for style, import order, and other linting by using:

```
tox -e lint
```

## Release management

To make a new release:

1. Go to https://github.com/cfpb/wagtail-flags/releases/new
1. Under the "Tag" drop-down, type the new version, incrementing the major, minor, or patch release digits as needed (for example, for a minor release on top of `5.4.0`, you'd enter `5.5.0`).
1. Click "Create new tag"
1. Leave target as `main`.
1. Set the "Release title" to the same as the new tag, (e.g. `5.5.0`).
1. Click "Generate release notes", make sure these look right.
1. Click "Publish release".
1. Under https://github.com/cfpb/wagtail-flags/actions, you should see a "Publish to PyPI" action running - observe it to make sure it completes without error.

If all worked correctly, you should see your new version at https://pypi.org/project/wagtail-flags/
