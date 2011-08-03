from django.conf.urls.defaults import *
import views


urlpatterns = patterns('dll.views',
    url(r'^(\d+)?$', views.home, name='dll.home'),
    url(r'^file/?$', views.create, name='dll.create'),
    url(r'^file/([a-zA-Z0-9\.]+)/?$', views.edit, name='dll.edit'),
    url(r'^search/?$', views.search, name='dll.search'),
)
