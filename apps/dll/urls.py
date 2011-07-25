from django.conf.urls.defaults import *


urlpatterns = patterns('dll.views',
    url(r'^$', 'home', name='dll.home'),
    url(r'^file/?$', 'create', name='dll.create'),
    url(r'^file/([a-zA-Z0-9\.]+)/?$', 'edit', name='dll.edit'),
    url(r'^search/?$', 'search', name='dll.search'),
)
