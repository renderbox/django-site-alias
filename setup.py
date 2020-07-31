# --------------------------------------------
# Copyright 2020, Grant Viklund
# @Author: Grant Viklund
# @Date:   2020-07-30 15:19:53
# --------------------------------------------

from os import path
from setuptools import setup, find_packages

file_path = path.abspath(path.dirname(__file__))

with open(path.join(file_path, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

package_metadata = {
    'name': 'django-site-aliases',
    'version': '0.1.0',
    'description': "A tool to support site aliases that wrap around Django's Site framework",
    'long_description': long_description,
    'url': 'https://github.com/renderbox/django-site-aliases/',
    'author': 'Grant Viklund',
    'author_email': 'renderbox@gmail.com',
    'license': 'MIT license',
    'classifiers': [
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    'keywords': ['django', 'app'],
}

setup(
    **package_metadata,
    packages=find_packages(),
    package_data={'sitealiases': ['*.html']},
    include_package_data=True,
    python_requires=">=3.6",
    install_requires=[
        'Django>=3.0,<3.1',
        'dj-database-url',
    ],
    extras_require={
        'dev': [
            'django-crispy-forms',
            'django-allauth',
        ],
        'test': [],
        'prod': [],
        'build': [
            'setuptools',
            'wheel',
            'twine',
        ],
        'docs': [
            'coverage',
            'Sphinx',
            'sphinx-bootstrap-theme',
            'sphinx-rtd-theme',
            'sphinx-js',
            'sphinx-autobuild',
        ],
    }
)