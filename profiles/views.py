from django.views.generic.simple import direct_to_template
from django.core.urlresolvers import reverse
from django.shortcuts import redirect, render_to_response
from django.template import RequestContext
from django.contrib.auth.models import User
from django.contrib.auth import logout, authenticate
from django.http import HttpResponseRedirect

from userena.forms import SignupForm
from userena.decorators import secure_required

from profiles.forms import ProfileForm
from profiles.models import Profile

@secure_required
def signup(request):
    if request.method == "POST":
        sform = SignupForm(request.POST)
        # pform = ProfileForm(request.POST, instance=Profile())
        if sform.is_valid(): # and pform.is_valid():
            user = sform.save()
            import pdb; pdb.set_trace()
            user = authenticate(username=request.POST['username'], 
                                password=request.POST['password1'])
            pform = ProfileForm(request.POST, instance=Profile())
            if pform.is_valid():
                import pdb; pdb.set_trace()
                profile = pform.save(commit=False)
                import pdb; pdb.set_trace()
                profile.user = user            
               # profile = pform.save()

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

