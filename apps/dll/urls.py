from django.conf.urls.defaults import *
import views


urlpatterns = patterns('dll.views',
    url(r'^(\d+)?$', views.home, name='dll.home'),
    url(r'^create/?$', views.create, name='dll.create'),
    url(r'^file/([\d]+)/?$', views.edit, name='dll.edit'),
    url(r'^view/([\d]+)/?$', views.view, name='dll.view'),
    url(r'^search/$', views.search, name='dll.search'),
)
