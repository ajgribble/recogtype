from django.conf.urls import patterns, include, url

from recogmatch import views as match_views

urlpatterns = patterns('',
    url(r'^(?P<username>[\.\w]+)/$', 
        match_views.dash,
        name='match_dash'),
)
