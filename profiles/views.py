from django.views.generic.simple import direct_to_template
from django.core.urlresolvers import reverse
from django.shortcuts import redirect, render_to_response
from django.template import RequestContext
from django.contrib.auth.models import User
from django.contrib.auth import logout, authenticate
from django.contrib import messages
from django.http import HttpResponseRedirect

from userena.forms import SignupForm
from userena.decorators import secure_required
from userena import views as userena_views

from profiles.forms import EditProfileFormMod
from profiles.models import Profile

from guardian.decorators import permission_required_or_403 

def signout(request):
   messages.success(request, 'Thank-you for your time! You\'ve been \
                              succesfully logged out.')
   logout(request)
   return HttpResponseRedirect('http://localhost:8000')


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
