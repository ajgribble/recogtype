from django import forms
from django.utils.translation import ugettext_lazy as _

class SubmitDataForm(forms.Form):
    """ Basic form to capture raw keystrokes from the user """
    
    KeyboardChoices=(
                            ('us_full', 'Standard US Full'),
                            ('us_lap', 'Standard US Laptop'),
                            ('uk_full', 'Standard UK Full'),
                            ('uk_lap', 'Standard UK Laptop'),
                            ('us_erg', 'Ergonomic US'),
                            ('uk_erg', 'Ergonomic UK'),
                            ('extended_full', 'Full With Non-English Characters'),
                            ('extended_lap', 'Laptop With Non-English Characters'),
                    )
    
    data = forms.CharField(label=_(u'Challenge Response'),
                           required=True,
                           widget=forms.Textarea(attrs={
                                                        'id': 'raw_data',
                                                        'form': 'raw_data_form',
                                                        'autofocus': 'autofocus',
                                                        'cols': 60,
                                                        'rows': 5
                                                        }
                                                )
                           )
    
    keyboard = forms.ChoiceField(label='Keyboard Type',
                                 choices=KeyboardChoices)
