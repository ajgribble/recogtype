from django.db import models
from django.contrib.auth.models import User

ChallengeTypeChoices=(
                        ('f', 'fixed'),
                        ('v', 'variable'),
                     )

ChallengeUseChoices=(
                        ('t', 'train'),
                        ('c', 'challenge'),
                    )

class Challenge(models.Model):
    title = models.CharField(max_length=50, verbose_name='Title')
    challenge_type = models.CharField(max_length=10, default='f', 
                                      choices=ChallengeTypeChoices,
                                      verbose_name='Challenge Type')
    challenge_use = models.CharField(max_length=10, default='t',
                                     choices=ChallengeUseChoices,
                                     verbose_name='Challenge Use')
    challenge_focus = models.CharField(max_length=300,
                                       verbose_name='Challenge Focus')
    instructions = models.TextField(verbose_name='Challenge Instructions')

    def __unicode__(self):
        return self.title 

class RawSample(models.Model):
    user = models.ForeignKey(User, verbose_name='Username')
    data = models.TextField(verbose_name='Raw Data')
    date_supplied = models.DateField(auto_now_add=True, verbose_name='Date Supplied')
    challenge_id = models.ForeignKey(Challenge, verbose_name='Challenge ID')
    os = models.CharField(max_length=25, verbose_name='OS')
    browser = models.CharField(max_length=50, verbose_name='Browser')
    keyboard = models.CharField(max_length=50, verbose_name="Keyboard")
    
class BioTemplate(models.Model):
    user = models.OneToOneField(User, unique=True, verbose_name='Username')
    bio_model = models.TextField(verbose_name='Bio Model')


