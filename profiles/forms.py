from django import forms
from django.utils.translation import ugettext_lazy as _
from django.forms.extras.widgets import SelectDateWidget

from userena.utils import get_profile_model

from profiles.models import Profile

class ProfileForm(forms.ModelForm):
    dob = forms.DateField(widget=SelectDateWidget(years=range(1994,1919,-1)))
    """
    def __init__(self, user, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
    """
    class Meta:
        model = Profile
        exclude = ['user']
    """
    def save(self, force_insert=False, force_update=False, commit=True):
        profile = super(ProfileForm, self).save(commit=commit)
        user = profile.user
        user.first_name = self.cleaned_data['first_name']
        user.dob = self.cleaned_data['dob']
        user.sex = self.cleaned_data['sex']
        user.handed = self.cleaned_data['handed']
        user.daily_usage = self.cleaned_data['daily_usage']
        user.save()

        return profile
    """
