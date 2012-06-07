from django.conf.urls import patterns, include, url

from recogmatch import views as match_views

urlpatterns = patterns('',
    url(r'^(?P<username>[\.\w]+)/biotemplate/(?P<challenge>[\-\w]+)/submit/$',
        match_views.submit_raw_data,
        name='match_submit'),
    url(r'^(?P<username>[\.\w]+)/biotemplate/(?P<challenge>[\-\w]+)/$',
        match_views.challenge,
        {'template_name': 'recogmatch/challenge_template.html'},
        name='match_train'),
    url(r'^(?P<username>[\.\w]+)/biotemplate/$',
        match_views.challenge,
        name='match_template'),
    url(r'^(?P<username>[\.\w]+)/$', 
        match_views.dash,
        name='match_dash'),
)
