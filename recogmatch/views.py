from django.views.generic.simple import direct_to_template
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from profiles.models import Profile

from datetime import date, timedelta

@login_required
def dash(request, username, template_name='recogmatch/dashboard.html',
         extra_context=None):

    # Initialize all variables to false as if they haven't been updated
    userName = False
    profileMug = False
    profileDob = False
    profileSex = False
    profileHand = False
    profileUse = False

    user = User.objects.get(username=username)
    userProfile = Profile.objects.get(user_id=user.id)
    
    if user.first_name != '':
        userName = True

    if userProfile.mugshot != '':
        profileMug = True
    
    if userProfile.dob <= date.today()-timedelta(days=6574.32):
        profileDob = True

    if userProfile.sex != '':
        profileSex = True

    if userProfile.handed != '':
        profileHand = True

    if userProfile.daily_usage != '':
        profileUse = True

    return direct_to_template(request,
                              template_name,
                              {'mug': profileMug, 'dob': profileDob,
                               'sex': profileSex, 'hand': profileHand,
                               'use': profileUse, 'name': userName})
