from recogmatch.models import Challenge
from django.contrib import admin
from django import forms

class ChallengeAdminForm(forms.ModelForm):
    ChallengeFocusChoices=(                    
                            ('first_letters', 'first letters'),
                            ('second_letters', 'second letters'),
                            ('third_letters', 'third letters'),
                            ('ending_letters', 'ending letters'),
                            ('digraphs', 'digraphs'),
                            ('trigraphs', 'trigraphs'),
                            ('doubles', 'doubles'),
                            ('common_2l_words', 'common 2l words'),
                            ('common_3l_words', 'common 3l words'),
                            ('common_4l_words', 'common 4l words'),
                            ('common_nl_words', 'common nl words'),
                         )
    challenge_focus = forms.MultipleChoiceField(choices=ChallengeFocusChoices,
                                                widget=forms.CheckboxSelectMultiple,
                                                initial='first_letters')

    class Meta:
        model = Challenge

class ChallengeAdmin(admin.ModelAdmin):
    form = ChallengeAdminForm

admin.site.register(Challenge, ChallengeAdmin)
