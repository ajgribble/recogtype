from django.views.generic.simple import direct_to_template
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from profiles.models import Profile

from datetime import date, timedelta

@login_required
def dash(request, username, template_name='recogmatch/dashboard.html',
         extra_context=None):

    # Initialize all variables to false as if they haven't been updated
    userObj = {'name': False, 'mug': False, 'dob': False,
            'sex': False, 'hand': False, 'use': False}

    user = User.objects.get(username=username)
    userProfile = Profile.objects.get(user_id=user.id)
    
    if user.first_name != '':
        userObj['name'] = True

    if userProfile.mugshot != '':
        userObj['mug'] = True
    
    if userProfile.dob <= date.today()-timedelta(days=6574.32):
        userObj['dob'] = True

    if userProfile.sex != '':
        userObj['sex'] = True

    if userProfile.handed != '':
        userObj['hand'] = True

    if userProfile.daily_usage != '':
        userObj['use'] = True

    return direct_to_template(request,
                              template_name,
                              userObj)

@login_required
def biotemplate(request, username, template_name='recogmatch/biotemplate.html'):
    
    return direct_to_template(request,
                              template_name)
