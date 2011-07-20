from django.conf.urls.defaults import *


urlpatterns = patterns('dll.views',
    url(r'^$', 'home', name='dll.home'),
    url(r'^(\d)/?$', 'edit', name='dll.edit')
#    url(r'^bleach/?$', 'bleach_test', name='examples.bleach'),
)
