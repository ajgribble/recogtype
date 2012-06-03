from django import forms
from django.utils.translation import ugettext_lazy as _

from recogmatch.models import Challenge, RawSample

class SubmitDataForm(forms.ModelForm):
    """ Basic form to capture raw keystrokes from the user """
    data = forms.CharField(label=_(u'Challenge Response'),
                              required=True)
    
    def __init__(self, *args, **kw):
        super(forms.ModelForm, self).__init__(*args, **kw)

    class Meta:
        model = RawSample
        exclude = ['user', 'date_supplied', 'challenge_id']

    def save(self, force_insert=False, force_update=False, commit=True):
        data = super(SubmitDataForm, self).save(commit=commit)

        return data
