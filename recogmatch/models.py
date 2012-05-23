from django.db import models
from django.contrib.auth.models import User

class Challenge(models.Model):
    title = models.CharField(max_length=30, verbose_name='Title')
    body = models.TextField(verbose_name='Challenge Request')

class RawSample(models.Model):
    user = models.ForeignKey(User, verbose_name='Username')
    data = models.TextField(verbose_name='Raw Data')
    date_supplied = models.DateField(auto_now_add=True, verbose_name='Date Supplied')
    challenge_id = models.ForeignKey(Challenge, verbose_name='Challenge ID')
    
class BioTemplate(models.Model):
    user = models.OneToOneField(User, unique=True, verbose_name='Username')
    bio_model = models.TextField(verbose_name='Bio Model')


