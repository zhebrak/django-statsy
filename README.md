
Django Statsy
========

[![Build Status](https://travis-ci.org/zhebrak/django-statsy.svg)](https://travis-ci.org/zhebrak/django-statsy) [![PyPI version](https://badge.fury.io/py/django-statsy.svg)](http://badge.fury.io/py/django-statsy)

Statsy is an application for collecting and displaying statistics in your Django project.


### Basic Usage

View decorator:

```python
@statsy.watch
def index(request):
    ...
```

```python
@statsy.watch(group='index', event='page_view')
def index(request):
    ...
```

Inside the view:

```python
def like(request):
  statsy.send(
    group='post', event='like', user=request.user,
    value=17, content_object=post
  )
  ...
```

CBV Mixin:

```python
class AboutView(WatchMixin, TemplateView):
    template_name = 'example/about.html'

    watch_group = 'info'
    watch_event = 'page_view'
    ...
```

From the template:

```javascript
{% load statsy %}

{% statsy %}

...

var statsy = new Statsy()

statsy.send({
  'group': 'post',
  'event': 'subscription'
});
```

### Installation

```
pip install django-statsy
```

```python
# settings.py

INSTALLED_APPS = (
  ...

  'statsy',
)
```

If you want to display collected statistics you will also have to add Statsy's URLs to your project's URLs.

```python
# urls.py
  ...

  url(r'^stats/', include('statsy.urls')),
  ...
```

### Dashboard

Default out of the box graphs.

![group_overview](https://raw.github.com/fata1ex/django-statsy/master/docs/img/overview_group.png)


### Configuration
There are some settings you may want to change (default values are specified).
```python
# settings.py

# By default Statsy caches lookups for a group and event
STATSY_CACHE_TIMEOUT = 60 * 15  # in seconds

# Statsy can work in async mode with Celery up and running
STATSY_ASYNC = False

# Full path to Celery application instance (e.g. 'example.celery_app.app')
CELERY_APP = None

# Permission to view stats pages
STATSY_VIEW_PERMISSION = 'statsy.stats_view'
```


### Collect Options

All are optional.
```python
# categorizing options
'group'
'event'

# some additional info about the stats object
'label'

# user associated with the action
# collected by default in @watch
'user'

# object of the action
'content_object'

# value can be <int>, <float> or <str>/<unicode>/etc.
'value'

# where did it happen
# collected by default in @watch
'url'

# how long did it take <int>
# collected by default in @watch
'duration'

# JSON for an extra data
'extra'
```

### Extending

If you want to add your custom stats page to Statsy you'll have to register it manually in "stats.py".

```python
# stats.py
import statsy

def some_awesome_stats(request):
    return render_to_response('app/awesome_stats.html')

statsy.site.register(some_awesome_stats)
```

You can also specify a category, a name or a permission

```python
statsy.site.register(
    some_awesome_stats,
    category='Awesome stats',
    name='Most awesome',
    permission='user.view_awesome_stats'
)
```

### Roadmap
- Enhanced statistics view
- More out of the box charts
- Aggregation over time
- User tracking
- Realtime statistics

### License
[MIT](https://github.com/fata1ex/django-statsy/raw/master/LICENSE)
