from django.views.generic.simple import direct_to_template
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.template.defaultfilters import slugify
from django.template import RequestContext
from django.shortcuts import render
from django.contrib import messages

from profiles.models import Profile
from recogmatch.models import Challenge, RawSample, BioTemplate
from recogmatch.forms import SubmitDataForm

from datetime import date, timedelta
from math import ceil

@login_required
def guide_user(request, username, template_name='recogmatch/dashboard.html',
         extra_context=None):

    def calculate_progress(progress):
        p_percent_complete = (float(progress['p_complete_count'])
                                        / progress['p_total_count'])* 100
        t_total_count = float(Challenge.objects.count())
        progress['t_challenges_needed'] = int(ceil((t_total_count * 2) / 3))        
        t_percent_complete = (float(progress['t_complete_count']) \
                                       / progress['t_challenges_needed']) * 100
        progress['overall_complete'] = (p_percent_complete + t_percent_complete)\
                                        / 2
        # Locks challenge link on nav panel if training isn't complete
        if progress['overall_complete'] == 100:
            pass
        elif progress['overall_complete'] >= 65:
            suggested.append('train')
            request.session['challenge_lock'] = False
        else:
            mandatory.append('train')
            request.session['challenge_lock'] = True
        
        return progress

    # Initialize attributes
    user = User.objects.get(username=username)
    mandatory = []
    suggested = []
    progress = {'overall_complete': 0,
                't_complete_count': 0,
                'p_total_count': 1} # Init at 1 for first_name in user obj

    user_profile = Profile.objects.get(user_id=user.id)
   
    # Go through each user/profile attribute to verify existence
    if user.first_name == '' :
        mandatory.append(key.replace('_', ' '))
    
    profile_ignore = ['mugshot', 'user_id', 'id', '_state', 'privacy']
    for key, val in user_profile.__dict__.iteritems():
        if key not in profile_ignore:
            progress['p_total_count'] = progress['p_total_count'] + 1
            if key == 'dob':
                if not val:
                    mandatory.append(key)
            elif key == 'language':
                if val == None:
                    mandatory.append(key)
            else:
                if val == '':
                    mandatory.append(key.replace('_', ' '))
    
    # Insert number of profile completion
    progress['p_complete_count'] = progress['p_total_count'] - len(mandatory)

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
 
        # Calls the calculate progress method to update the progress dictionary
        progress = calculate_progress(progress)
        
    else:
        request.session['train_lock'] = True
        request.session['challenge_lock'] = True
        
        # Calls the calculate progress method to update the progress dictionary
        progress = calculate_progress(progress)

    return direct_to_template(request, template_name,
                             {'mandatory': mandatory,
                              'suggested': suggested,
                              'progress': progress})

@login_required
def challenge(request, username, challenge=None,
              template_name='recogmatch/biotemplate.html'):
    
    user = User.objects.get(username=username)
    challenge_list = Challenge.objects.filter(challenge_use='t')
    data_form = SubmitDataForm()

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
            return render(request, template_name,
                                     {'challenge': item,
                                      'url_title': url_title,
                                      'template_path': template_path,
                                      'data_form': data_form})                                

    return direct_to_template(request, template_name,
                             {'url_chunks': url_chunks,
                              'completed': challenges_complete})

@login_required
@csrf_exempt
def submit_raw_data(request, username, challenge_id):
    sample = RawSample()
    sample.user = User.objects.get(username=username)
    sample.data = request.POST['raw_data']
    sample.challenge_id = Challenge.objects.get(id=challenge_id)
    sample.browser = request.POST['browser']
    sample.os = request.POST['os']
    sample.keyboard = request.POST['keyboard']
    sample.save()
    messages.success(request, 'Challenge complete!')
    
    return HttpResponse("Success")
    
