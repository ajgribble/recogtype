from django.views.generic.simple import direct_to_template
from django.core.urlresolvers import reverse
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext as _

from userena.forms import EditProfileForm
from userena.decorators import secure_required
from userena import views as userena_views
from userena.utils import get_profile_model
from userena import settings as userena_settings

from profiles.models import Profile

from recogmatch.views import guide_user

from guardian.decorators import permission_required_or_403 

import json

@login_required
def signout(request):
   messages.success(request, 'Thank you for your time! You\'ve been \
                              succesfully logged out.')
   logout(request)
   return HttpResponseRedirect('/')

@secure_required
@permission_required_or_403('change_profile', (get_profile_model(), 'user__username', 'username'))
def profile_edit(request, username, edit_profile_form=EditProfileForm,
                 template_name='userena/profile_form.html', success_url=None,
                 extra_context=None):

    # Copied from Userena views to work around decorator issue
    user = get_object_or_404(User,
                             username__iexact=username)

    profile = user.get_profile()

    user_initial = {'first_name': user.first_name,
                    'last_name': user.last_name}

    form = edit_profile_form(instance=profile, initial=user_initial)

    if request.method == 'POST':
        form = edit_profile_form(request.POST, request.FILES, instance=profile,
                                 initial=user_initial)

        if form.is_valid():
            profile = form.save()
            
            # Updates nav pane
            guide_user(request, username)
            
            if userena_settings.USERENA_USE_MESSAGES:
                messages.success(request, _('Your profile has been updated.'),
                                 fail_silently=True)

            if success_url: 
                redirect_to = success_url % {'username': user.username }
            else: 
                redirect_to = reverse('userena_profile_detail', 
                kwargs={'username': username})
            return redirect(redirect_to)

    if not extra_context: extra_context = dict()
    extra_context['form'] = form
    extra_context['profile'] = profile
    
    
    return direct_to_template(request,
                              template_name,
                              extra_context=extra_context)

def get_user_stats(request):
    user_count = Profile.objects.count()
    country_count = Profile.objects.values_list('country').distinct().count()
    language_count = Profile.objects.values_list('language').distinct().count()
    counts = json.dumps({
                            'users': user_count,
                            'countries': country_count,
                            'languages': language_count
                        })

    return HttpResponse(counts)

def verify_email(request):
    email_existence = User.objects.filter(email=request.POST['email']).exists()

    return HttpResponse(email_existence)
