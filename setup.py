from setuptools import find_packages, setup


long_description = open('README.md', 'r').read()

install_requires = [
    'wagtail>=1.13,<2.9',
    'django-flags>=4.2,<5.0'
]

testing_extras = [
    'coverage>=3.7.0',
]

setup(
    name='wagtail-flags',
    url='https://github.com/cfpb/wagtail-flags',
    author='CFPB',
    author_email='tech@cfpb.gov',
    description='Feature flags for Wagtail sites',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='CC0',
    version='4.1.0',
    include_package_data=True,
    packages=find_packages(),
    install_requires=install_requires,
    extras_require={
        'testing': testing_extras,
    },
    classifiers=[
        'Framework :: Django',
        'Framework :: Django :: 1.11',
        'Framework :: Django :: 2.0',
        'Framework :: Django :: 2.1',
        'Framework :: Django :: 2.2',
        'Framework :: Wagtail',
        'Framework :: Wagtail :: 1',
        'Framework :: Wagtail :: 2',
        'License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication',
        'License :: Public Domain',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
    ]
)
