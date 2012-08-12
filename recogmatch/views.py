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
from django.conf import settings

from profiles.models import Profile

from recogmatch.models import Challenge, RawSample, BioTemplate
from recogmatch.forms import SubmitDataForm

from recogtype_backend import RecogDataSample, RecogNoveltyDetector

from datetime import date, timedelta
from math import ceil

@login_required
def guide_user(request, username, template_name='recogmatch/dashboard.html',
         result_mod=None):

    # Method to calculate the progress done by the user where 
    # p variables for profile, t for training and c for challenging
    def calculate_progress(p_complete_count, p_total_count, t_complete_count, 
                           user, suggested, mandatory):
        progress = {} 

        # Profile calculations
        p_percent_complete = (float(p_complete_count)
                                        / p_total_count)* 100

        # Training calculations
        t_total_count = float(Challenge.objects.filter(challenge_use='t').count())
        progress['t_challenges_needed'] = int(ceil((t_total_count * 2) / 3))        
        progress['t_challenges_left'] = progress['t_challenges_needed'] - \
                                            t_complete_count
        t_percent_complete = (float(t_complete_count) \
                                       / progress['t_challenges_needed']) * 100

        # Testing (challenging) calculations done if training is complete
        if progress['t_challenges_left'] <= 0:
            try:
                testing_ids = []
                for item in Challenge.objects.filter(challenge_use='c'):
                    testing_ids.append(item.id)

                c_complete_count = RawSample.objects.filter(
                                                        user_id=user.id,
                                                        challenge_id_id__in=testing_ids
                                                        ) \
                                                    .distinct().count()
            except ObjectDoesNotExist:             
                c_complete_count = 0

            c_total_count = float(Challenge.objects.filter(challenge_use='c').count())
            progress['c_challenges_needed'] = int(c_total_count * 5)
            progress['c_challenges_left'] = progress['c_challenges_needed'] - \
                                                c_complete_count
            c_percent_complete = (float(c_complete_count) \
                                           / progress['c_challenges_needed']) * 100

            # Decides whether challenging is mandatory or suggested
            if progress['c_challenges_left'] > 0:
                mandatory.append('test')
            else:
                suggested.append('test')
        else:
            c_percent_complete = 0

        # Overall progress complete
        progress['overall_complete'] = (p_percent_complete + t_percent_complete \
                                        + c_percent_complete) / 3

        # Locks challenge link on nav panel if training isn't complete
        if p_percent_complete == 100:
            # request.session['challenge_lock'] = False
            if progress['t_challenges_left'] <= 0:
                if t_complete_count < t_total_count:
                    suggested.append('train')
                request.session['challenge_lock'] = False
            else:
                mandatory.append('train')
        
        return progress

    # Initialize attributes
    user = User.objects.get(username=username)
    mandatory = []
    suggested = []
    p_total_count = 1 # Init at 1 for first_name in user obj
    t_complete_count = 0
    c_complete_count = 0
    user_profile = Profile.objects.get(user_id=user.id)

    # Training and challenging are both initially locked
    request.session['train_lock'] = True
    request.session['challenge_lock'] = True
   
    # Go through each user/profile attribute to verify existence
    if user.first_name == '' :
        mandatory.append('first name')
    
    profile_ignore = ['mugshot', 'user_id', 'id', '_state', 'privacy']
    for key, val in user_profile.__dict__.iteritems():
        if key not in profile_ignore:
            p_total_count = p_total_count + 1
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
    p_complete_count = p_total_count - len(mandatory)

    # Update session to reflect navigation panel
    request.session['profile_count'] = len(mandatory)

    # If mandatory profile is fully updated, allow training
    if request.session['profile_count'] == 0:
        request.session['train_lock'] = False
        try:
            training_ids = []
            for item in Challenge.objects.filter(challenge_use='t'):
                training_ids.append(item.id)

            t_complete_count = RawSample.objects.filter(
                                                    user_id=user.id,
                                                    challenge_id_id__in=training_ids
                                                    ) \
                                                .distinct().count()
        except ObjectDoesNotExist:             
            t_complete_count = 0
    
    # Calls the calculate progress method to update the progress dictionary
    progress = calculate_progress(p_complete_count, p_total_count, 
               t_complete_count, user, suggested, mandatory)

    # If redirected from a previous training challenge extract and 
    # manipulate the results.
    # $$ Incredibly inefficient and will eventually be changed
    if result_mod:
        result = {}
        
        result_mod = result_mod.split('&')

        # Create a generic score
        result['fail'] = int(result_mod[0])
        result['pass'] = int(result_mod[1])
        total = result['fail'] + result['pass']
        result['percent_pass'] = round(result['pass'] / float(total) * 100)
        if result['percent_pass'] >= 95:
            result['score'] = 'high pass'
        elif result['percent_pass'] >= 90:
            result['score'] = 'possible pass'
        elif result['percent_pass'] >= 85:
            result['score'] = 'border line fail'
        else:
            result['score'] = 'fail'

    return direct_to_template(request, template_name,
                             {'mandatory': mandatory,
                              'suggested': suggested,
                              'progress': progress,
                              'result': result})

@login_required
def challenge(request, username, model_action, challenge=None,
              template_name='recogmatch/challenge_list.html'):
    
    user = User.objects.get(username=username)
    challenge_ids = []

    # If user is training system challenge_use is t, if challenging it's c
    if model_action == 'train':
        challenge_list = Challenge.objects.filter(challenge_use='t')
    else:
        challenge_list = Challenge.objects.filter(challenge_use='c')
    
    for item in challenge_list:
        challenge_ids.append(item.id)

    data_form = SubmitDataForm()

    url_chunks = {}
    challenges_complete = []

    for item in challenge_list:
        url_title = slugify(item)
        url_chunks[item.title] = url_title
        template_path = 'recogmatch/challenges/' + url_title + '.html'
     
        if challenge == url_title: 
            return render(request, template_name,
                                     {'challenge': item,
                                      'url_title': url_title,
                                      'template_path': template_path,
                                      'data_form': data_form,
                                      'model_action': model_action})                                

        # If training challenge is complete add to completed list
        if model_action == 'train':
            if RawSample.objects.filter(user_id=user.id, challenge_id=item.id,
                                        challenge_id_id__in=challenge_ids).exists():
                challenges_complete.append(item.title)
        

    return direct_to_template(request, template_name,
                             {'url_chunks': url_chunks,
                              'completed': challenges_complete,
                              'model_action': model_action})

@login_required
@csrf_exempt
def submit_raw_data(request, username, challenge_id):

    # From the submitted challenge, the raw data object is created and stored 
    # for future use.
    sample = RawSample()
    sample.user = User.objects.get(username=username)
    sample.data = request.POST['raw_data']
    sample.challenge_id = Challenge.objects.get(id=challenge_id)
    sample.browser = request.POST['browser']
    sample.os = request.POST['os']
    sample.keyboard = request.POST['keyboard']
    sample.save()
    messages.success(request, 'Challenge complete!')

    # After the raw data has been saved action is taken: train or challenge
    if request.POST['model_action'] == 'challenge':
        test_data = sample.data
        
        try:
            training_ids = []
            train_data = []
            for item in Challenge.objects.filter(challenge_use='t'):
                training_ids.append(item.id)

            rss = RawSample.objects.filter(
                                            user_id=sample.user.id,
                                            challenge_id_id__in=training_ids
                                          )
            for item in rss.iterator():
                train_data.append(item.data)

        except ObjectDoesNotExist:             
            train_data = ''
        
        # Specific svm params for single class svm 
        params = {
                    'nu': 0.1,
                    'kernel': 'linear'}

        # Initialize the novelty detector
        rnd = RecogNoveltyDetector(sample.user.id)
        result = rnd.challenge(train_data,
                               test_data,
                               settings.RECOGTYPE_KS_EXAMINED, 
                               settings.RECOGTYPE_FEATURE_LIST,
                               params)

        # Modify result so it's not passed in the clear
        result_mod = str(result[0]) + '&' + str(result[1])
        
        # Not currently saving model in the db because it cannot be rebuilt
        """
        # Check if a model has already been created for the user
        # If there is no current model, create one
        try:
            current_model = BioTemplate.objects.get(user_id=sample.user.id)
        except:
            current_model = BioTemplate()
            current_model.user_id = sample.user.id

        current_model.bio_model = model
        current_model.save()
        """
    return HttpResponse(result_mod)
    
