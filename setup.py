# --------------------------------------------
# Copyright 2020, Grant Viklund
# @Author: Grant Viklund
# @Date:   2020-07-30 15:19:53
# --------------------------------------------

from os import path
from setuptools import setup, find_packages

# from sitealiases.__version__ import VERSION

readme_file = path.join(path.dirname(path.abspath(__file__)), 'README.md')

try:
    from m2r import parse_from_file
    long_description = parse_from_file(readme_file)     # Convert the file to RST for PyPI
except ImportError:
    # m2r may not be installed in user environment
    with open(readme_file) as f:
        long_description = f.read()

package_metadata = {
    'name': 'django-site-aliases',
    'version': '0.1.2',
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
    package_data={'sitealias': ['*.html']},
    include_package_data=True,
    python_requires=">=3.6",
    install_requires=[
        'Django>=3.0,<4.1',
        'dj-database-url',
        'django-crispy-forms',
    ],
    extras_require={
        'dev': [
            'django-allauth',
        ],
        'test': [],
        'prod': [],
        'build': [                          # Packages needed to build the package
            'setuptools',
            'wheel',
            'twine',
            'm2r',
        ],
        'docs': [                           # Packages needed to generate docs
            'm2r',
            'coverage',
            'Sphinx',
            'sphinx-bootstrap-theme',
            'sphinx-rtd-theme',  # Assumes a Read The Docs theme for opensource projects
            'sphinx-js',
            'sphinx-autobuild',
        ],
    }
)