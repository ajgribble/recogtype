from django.conf.urls import patterns, include, url
from django.views.generic.simple import direct_to_template
from django.contrib.auth import views as auth_views

from profiles.forms import EditProfileFormMod 

from userena import views as userena_views
from userena import settings as userena_settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', direct_to_template, {
        'template': 'homepage.html',
    }, name='home'),

    # Basic Account Links
    url(r'^signup/', 
        userena_views.signup, 
        name='userena_signup'),
    url(r'^signin/',
        userena_views.signin,
        name='userena_signin'),
    url(r'^signout/',
        auth_views.logout,
        {'next_page': userena_settings.USERENA_REDIRECT_ON_SIGNOUT,
         'template_name': 'userena/signout.html'},
        name='userena_signout'),
    url(r'^profiles/(?P<username>[\.\w]+)/edit/$',
        userena_views.profile_edit,
        {'edit_profile_form': EditProfileFormMod},
        name='userena_signup'),

    # Directive Package URLs
    url(r'^profiles/', include('userena.urls')),
    url(r'^dashboard/', include('recogmatch.urls')),   
    
    url(r'^recogadmin/', include(admin.site.urls)),
)
