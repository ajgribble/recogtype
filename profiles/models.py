from django.db import models
from django.contrib.auth.models import User
from userena.models import UserenaBaseProfile

import datetime

GENDER_CHOICES = (
        ('M', 'Male'),
	('F', 'Female'),
)

HAND_CHOICES = (
	('R', 'Right'),
	('L', 'Left'),
	('A', 'Ambidextrous'),
)

HOUR_CHOICES = (
	('<1', 'Less Than 1'),
	('1-2', 'Between 1 and 2'),
	('2-5', 'Between 2 and 5'),
	('>5', 'Greater Than 5'),
)

class Profile(UserenaBaseProfile):
    user = models.OneToOneField(User, unique=True, verbose_name='Username', 
		    		related_name='profile')
    dob = models.DateField(default=datetime.date.today, blank=True)
    sex = models.CharField(verbose_name='Sex', max_length=1, blank=True,
                           choices=GENDER_CHOICES)
    handed = models.CharField(verbose_name='Handedness', max_length=1, 
		    	              blank=True, choices=HAND_CHOICES)
    daily_usage = models.CharField(verbose_name='Daily PC Usage', max_length=10,
		  		                   blank=True, choices=HOUR_CHOICES)
