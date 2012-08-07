from django.views.generic.simple import direct_to_template
from django.core.urlresolvers import reverse
from django.shortcuts import redirect, render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.models import User
from django.contrib.auth import logout, authenticate
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext as _

from userena.forms import SignupForm, EditProfileForm
from userena.decorators import secure_required
from userena import views as userena_views
from userena.utils import get_profile_model
from userena import settings as userena_settings

from profiles.forms import EditProfileFormMod
from profiles.models import Profile

from recogmatch.views import guide_user

from guardian.decorators import permission_required_or_403 

@login_required
def signout(request):
   messages.success(request, 'Thank-you for your time! You\'ve been \
                              succesfully logged out.')
   logout(request)
   return HttpResponseRedirect('/')

"""
@secure_required
def signup(request):
    if request.method == "POST":
        sform = SignupForm(request.POST)
        # pform = ProfileForm(request.POST, instance=Profile())
        if sform.is_valid(): # and pform.is_valid():
            user = sform.save()
            user = authenticate(username=request.POST['username'], 
                                password=request.POST['password1'])
            pform = ProfileForm(request.POST, instance=Profile())
            if pform.is_valid():
                profile = pform.save(commit=False)
                profile.user = user
                profile = pform.save()
   
            messages.success(request, 'Registration complete!')

            redirect_to = reverse('userena_signup_complete',
                                  kwargs={'username': user.username})

            if request.user.is_authenticated():
                logout(request)
            return redirect(redirect_to)

    else:
        sform = SignupForm()
        pform = ProfileForm()
        
    return render_to_response('profiles/signup_form.html', {'sform': sform,
                                                               'pform': pform},
                                  context_instance=RequestContext(request))
"""
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

            if success_url: redirect_to = success_url
            else: redirect_to = reverse('userena_profile_detail', kwargs={'username': username})
            return redirect(redirect_to)

    if not extra_context: extra_context = dict()
    extra_context['form'] = form
    extra_context['profile'] = profile
    
    
    return direct_to_template(request,
                              template_name,
                              extra_context=extra_context)
