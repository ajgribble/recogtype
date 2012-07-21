from django.views.generic.simple import direct_to_template
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.template.defaultfilters import slugify

from profiles.models import Profile
from recogmatch.models import Challenge, RawSample, BioTemplate
from recogmatch.forms import SubmitDataForm

from datetime import date, timedelta

@login_required
def guide_user(request, username, template_name='recogmatch/dashboard.html',
         extra_context=None):

    # Initialize user object
    user = User.objects.get(username=username)
    mandatory_profile = {}
    suggested_profile = {}
    user_profile = Profile.objects.get(user_id=user.id)
    bio_template = False
    
    if user.first_name == '':
        mandatory_profile['first name'] = True

    if user_profile.mugshot == '':
        suggested_profile['mug shot'] = True
   
    if user_profile.dob:
        if user_profile.dob >= date.today()-timedelta(days=6574.32):
            mandatory_profile['date of birth'] = True
    else:
        mandatory_profile['date of birth'] = True

    if user_profile.sex == '':
        mandatory_profile['sex'] = True

    if user_profile.handed == '':
        mandatory_profile['handedness'] = True

    if user_profile.daily_usage == '':
        mandatory_profile['daily computer usage'] = True

    if user_profile.country == '':
        mandatory_profile['country'] = True
    
    if user_profile.language == None:
        mandatory_profile['first language'] = True

    request.session['profile_count'] = len(mandatory_profile)

    if request.session['profile_count'] == 0:
        try:
            user_template = BioTemplate.objects.get(user_id=user.id)
        except ObjectDoesNotExist:             
            bio_template = True

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
        url_title = slugify(item)
        url_chunks[item.title] = url_title
        template_path = 'recogmatch/challenges/' + url_title + '.html'
     
        if challenge == url_title: 
            return direct_to_template(request, template_name,
                                     {'challenge': item,
                                      'url_title': url_title,
                                      'template_path': template_path})                                

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
    
