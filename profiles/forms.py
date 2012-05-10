from django import forms
from django.utils.translation import ugettext_lazy as _
from django.forms.extras.widgets import SelectDateWidget

from profiles.models import Profile

from userena.utils import get_profile_model

# Overrides userena's built in profile
class EditProfileFormMod(forms.ModelForm):
    first_name = forms.CharField(label=_(u'first Name'),
                                         max_length=30)
    dob = forms.DateField(widget=SelectDateWidget(years=range(1994,1919,-1)))
    
    def __init__(self, *args, **kw):
        super(forms.ModelForm, self).__init__(*args, **kw)
        # Remove the ability to input last name and privacy
        self.fields.pop('privacy')
        # Move first name to top of list
        new_order = self.fields.keyOrder[:-1]
        new_order.insert(0, 'first_name')
        mug_key = new_order.index('mugshot')
        new_order.append('mugshot')
        new_order.pop(mug_key) 
        self.fields.keyOrder = new_order
    
    class Meta:
        model = get_profile_model()
        exclude = ['user']

    def save(self, force_insert=False, force_update=False, commit=True):
        profile = super(EditProfileFormMod, self).save(commit=commit)
        # Save first name
        user = profile.user
        user.first_name = self.cleaned_data['first_name']
        user.save()

        return profile
