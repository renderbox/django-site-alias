# Django Site Alias

A Django App to add support for domain aliases to entries in  Django's Site framework.  

## The Problem

For example, your platform might create the FQDN for your customer like this:

```
customer.myplatform.com
```

They might want to use the domain name of:

```
customersite.com
```

The problem with Django's site framework is: 1 Domain = 1 Site ID

There are two ways to solve this.  The first is to create an instance per customer that manually sets the SITE_ID.  They then go to that instance running the app and it works.  The downside is that you are provisioning a server per customer, which can get inefficient at scale.

What if you have multiple customers but waitn to maintain only one server?

The alternate to setting a SITE_ID explicitly is to use Django's middleware to figure out the site from the request.  This is fine, if there is only one possible domain per customer.

## Solution 

To try to resolve this issue we created some lite 'wrapper' code around the Site framework to provide an alias lookup.

It's in a seperate model that you can let your customers update if you want (via a customer admin panel for example), letting them update as they want while keeping the Site model out of their hands.

## Setup

To install run the following in a shell:

```bash
pip install django-site-alias
```

then add 'sitealias' to your django project's list of apps and run migrate to get the new model.  Make sure to also include 'django.contrib.sites' since this is just a wraper around that code.
## Builtin View Mixins
**PassRequestToFormKwargsMixin** - adds the current request to the form kwargs

**SetSiteFromRequestFormValidMixin** - sets the current site to the self.object.site with in the form_valid of any generic editing view

**SiteQuerysetMixin:** - django-rest-framwork view mixin: Filters model by current site found in the request.


## Built-in managers

```python
from sitalias.models import RequestSiteManager

class Model(models.Model):
 #......
    objects = RequestSiteManager()
``` 

Will add the following chainable methods to the objects filter:

```python
Model.objects.from_site(site)
```
or

```python
Model.objects.from_request(request)
```

Included manager serves as a suggestion, feel free to build your own implementation.

## Roadmap

- [x] Middleware - sitealias.middleware.CurrentSite - mimics to `django.contrib.sites.middleware.CurrentSite` except that it adds current `site` to `request` object site via Sitealias model, before checking the Site table 
- [x] Shortcut - `from sitealias.shortcuts import get_current_site` - mimics `django.contrib.sites.shortcuts.get_current_site` but checks sitealias table before checking the Site model
- [] Callables for the ALLOWED_HOSTS setting (perhaps a subclass of the AllowedSites callable in [django-allowedsites](https://github.com/kezabelle/django-allowedsites) ?? )
    - [] CachedAllowedSitesAndAlias
    - [] AllowedSitesAndAliass ??
    
```python
INSTALLED_APPS = [
    ...
    'django.contrib.sites',
    ...
    'sitealias',
    ...
]
```

Then in your Django settings, add the following to your middleware:

```python
MIDDLEWARE = [
    ...
    'sitealias.middleware.CurrentSiteMiddleware',
    ...
]

```
This is meant to be a drop-in replacement for Django's 'django.contrib.sites.middleware.CurrentSiteMiddleware'.  It will look for a site that matches an alias first, then fall back to Django's code.
