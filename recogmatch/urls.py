from django.conf.urls import patterns, include, url

from recogmatch import views as match_views

urlpatterns = patterns('',
    url(r'^(?P<username>[\.\w]+)/biotemplate/(?P<challenge>[\-\w]+)/$',
        match_views.build_template,
        {'template_name': 'recogmatch/challenge_template.html'},
        name='match_train'),
    url(r'^(?P<username>[\.\w]+)/biotemplate/$',
        match_views.build_template,
        name='match_template'),
    url(r'^(?P<username>[\.\w]+)/$', 
        match_views.dash,
        name='match_dash'),
)
