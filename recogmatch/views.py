from django.views.generic.simple import direct_to_template
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from profiles.models import Profile
from recogmatch.models import Challenge, RawSample, BioTemplate
from recogmatch.forms import SubmitDataForm

from datetime import date, timedelta

@login_required
def dash(request, username, template_name='recogmatch/dashboard.html',
         extra_context=None):

    # Initialize all variables to decide what to advise to the user
    mandatory_profile = {}
    suggested_profile = {}
    user = User.objects.get(username=username)

    def profile_update(mandatory_profile, suggested_profile, user):

        user_profile = Profile.objects.get(user_id=user.id)
        
        if user.first_name == '':
            mandatory_profile['first name'] = True

        if user_profile.mugshot == '':
            suggested_profile['mug shot'] = True
        
        if user_profile.dob >= date.today()-timedelta(days=6574.32):
            mandatory_profile['date of birth'] = True

        if user_profile.sex == '':
            mandatory_profile['sex'] = True

        if user_profile.handed == '':
            mandatory_profile['handedness'] = True

        if user_profile.daily_usage == '':
            mandatory_profile['daily computer usage'] = True

        return mandatory_profile, suggested_profile

    def bio_template_update(mandatory_profile, user):
        
        for key, val in mandatory_profile.items():
            if key:
                return
        
        try:
            user_template = BioTemplate.objects.get(user_id=user.id)
        except ObjectDoesNotExist:             
            bio_template = True
            return bio_template

    (mandatory_profile, suggested_profile) = profile_update(mandatory_profile, 
                                                    suggested_profile,
                                                    user)
    bio_template = bio_template_update(mandatory_profile, user)
    
    return direct_to_template(request, template_name,
                             {'mandatory': mandatory_profile,
                              'suggested': suggested_profile,
                              'bio_template': bio_template})

@login_required
def challenge(request, username, challenge=None,
              template_name='recogmatch/biotemplate.html'):
    
    user = User.objects.get(username=username)
    challenges = Challenge.objects.all()

    url_chunks = {}

    for item in challenges:
        url_title = item.title.split(': ')
        url_title = url_title[1].replace(' ', '-')
        url_chunks[item.title] = url_title
     
        if challenge == url_title: 
            return direct_to_template(request, template_name,
                                     {'challenge': item,
                                      'url_title': url_title})                                

    return direct_to_template(request, template_name,
                             {'url_chunks': url_chunks})
@login_required
@csrf_exempt
def submit_raw_data(request, username, challenge_id):
    raw_data = request.POST['data']
    user = User.objects.get(username=username)
    challenge = Challenge.objects.get(id=challenge_id)

    sample = RawSample()
    sample.user = user
    sample.data = raw_data
    sample.challenge_id=challenge
    sample.save()

    return HttpResponse(raw_data)
    
