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
from math import ceil

@login_required
def guide_user(request, username, template_name='recogmatch/dashboard.html',
         extra_context=None):

    # Initialize attributes
    user = User.objects.get(username=username)
    mandatory = {}
    suggested = {}
    progress = {}
    user_profile = Profile.objects.get(user_id=user.id)
   
    # Go through each profile attribute to verify existence
    if user.first_name == '':
        mandatory['first name'] = True

    if user_profile.mugshot == '':
        suggested['mug shot'] = True
   
    if user_profile.dob:
        if user_profile.dob >= date.today()-timedelta(days=6574.32):
            mandatory['date of birth'] = True
    else:
        mandatory['date of birth'] = True

    if user_profile.sex == '':
        mandatory['sex'] = True

    if user_profile.handed == '':
        mandatory['handedness'] = True

    if user_profile.daily_usage == '':
        mandatory['daily computer usage'] = True

    if user_profile.country == '':
        mandatory['country'] = True
    
    if user_profile.language == None:
        mandatory['first language'] = True

    # Update session to reflect navigation panel
    request.session['profile_count'] = len(mandatory)

    # If mandatory profile is fully updated, allow training
    if request.session['profile_count'] == 0:
        request.session['train_lock'] = False
        try:
            progress['t_complete_count'] = RawSample.objects.filter(user_id=user.id
                                                           ).distinct(
                                                           ).count(
                                                           )
        except ObjectDoesNotExist:             
            progress['t_complete_count'] = 0

        t_total_count = float(Challenge.objects.count())
        progress['t_challenges_needed'] = int(ceil((t_total_count * 2) / 3))
        progress['t_challenge_difference'] = progress['t_challenges_needed'] - \
                                                progress['t_complete_count']
        progress['t_percent_complete'] = progress['t_complete_count'] \
                                                / t_total_count * 100
        
        # Locks challenge link on nav panel if training isn't complete
        if progress['t_percent_complete'] == 100:
            pass
        elif progress['t_percent_complete'] >= 65:
            suggested['train'] = True
            request.session['challenge_lock'] = False
        else:
            mandatory['train'] = True
            request.session['challenge_lock'] = True
    else:
        request.session['train_lock'] = True
        request.session['challenge_lock'] = True

    return direct_to_template(request, template_name,
                             {'mandatory': mandatory,
                              'suggested': suggested,
                              'progress': progress})

@login_required
def challenge(request, username, challenge=None,
              template_name='recogmatch/biotemplate.html'):
    
    user = User.objects.get(username=username)
    challenge_list = Challenge.objects.filter(challenge_use='t')

    url_chunks = {}
    challenges_complete = []

    for item in challenge_list:
        url_title = slugify(item)
        url_chunks[item.title] = url_title
        template_path = 'recogmatch/challenges/' + url_title + '.html'
     
        # If challenge is complete add to completed list
        if RawSample.objects.filter(user_id=user.id, challenge_id=item.id).exists():
            challenges_complete.append(item.title)
        
        if challenge == url_title: 
            return direct_to_template(request, template_name,
                                     {'challenge': item,
                                      'url_title': url_title,
                                      'template_path': template_path})                                

    return direct_to_template(request, template_name,
                             {'url_chunks': url_chunks,
                              'completed': challenges_complete})

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
    
