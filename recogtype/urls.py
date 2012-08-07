from django.conf.urls import patterns, include, url
from django.views.generic.simple import direct_to_template
from django.contrib.auth import views as auth_views

from profiles.forms import EditProfileFormMod 
from profiles import views as profiles_views

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
        profiles_views.signout,
        name='profiles_signout'),
    url(r'^profiles/(?P<username>[\.\w]+)/edit/$',
        profiles_views.profile_edit,
        {'edit_profile_form': EditProfileFormMod},
        name='profiles_edit'),

    # Activate
    url(r'^profiles/activate/(?P<activation_key>\w+)/$',
       userena_views.activate,
       {'success_url': '/dashboard/%(username)s'}, 
       name='profiles_activate'),

    # Reset password
    url(r'^password/reset/$',
       auth_views.password_reset,
       {'template_name': 'userena/password_reset_form.html',
        'email_template_name': 'userena/emails/password_reset_message.txt'},
       name='userena_password_reset'),
    url(r'^profiles/password/reset/done/$',
       auth_views.password_reset_done,
       {'template_name': 'profiles/password_reset_done.html'},
       name='profiles_password_reset_done'),
    url(r'^password/reset/confirm/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$',
       auth_views.password_reset_confirm,
       {'template_name': 'userena/password_reset_confirm_form.html'},
       name='userena_password_reset_confirm'),
    url(r'^password/reset/confirm/complete/$',
       auth_views.password_reset_complete,
       {'template_name': 'userena/password_reset_complete.html'}),

    # Change password
    url(r'^(?P<username>[\.\w]+)/password/$',
       userena_views.password_change,
       name='userena_password_change'),
    url(r'^profiles/(?P<username>[\.\w]+)/password/complete/$',
       userena_views.direct_to_user_template,
       {'template_name': 'profiles/password_complete.html'},
       name='profiles_password_change_complete'),
    
    # Directive Package URLs
    url(r'^profiles/', include('userena.urls')),
    url(r'^dashboard/', include('recogmatch.urls')),   
    
    # Admin
    url(r'^recogadmin/', include(admin.site.urls)),
)
