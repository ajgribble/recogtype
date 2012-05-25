from django.views.generic.simple import direct_to_template
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from profiles.models import Profile

@login_required
def dash(request, username, template_name='recogmatch/dashboard.html',
         extra_context=None):

    

    return direct_to_template(request,
                              template_name,
                              {'tester': username})
