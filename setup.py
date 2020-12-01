from setuptools import find_packages, setup

install_requires = [
    "wagtail>=2.7,<3",
    "django-flags>=4.2,<5.1",
]

testing_extras = ["coverage>=3.7.0"]

setup(
    name="wagtail-flags",
    url="https://github.com/cfpb/wagtail-flags",
    author="CFPB",
    author_email="tech@cfpb.gov",
    description="Feature flags for Wagtail sites",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    license="CC0",
    version="5.0.0",
    include_package_data=True,
    packages=find_packages(),
    python_requires=">=3.6",
    install_requires=install_requires,
    extras_require={"testing": testing_extras},
    classifiers=[
        "Framework :: Django",
        "Framework :: Django :: 2.2",
        "Framework :: Django :: 3.1",
        "Framework :: Wagtail",
        "Framework :: Wagtail :: 2",
        "License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication",
        "License :: Public Domain",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
    ],
)
