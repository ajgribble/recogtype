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
    first_name = models.CharField(verbose_name='First Name', max_length=50)
    dob = models.DateField(default=datetime.date.today)
    sex = models.CharField(verbose_name='Sex', max_length=1, choices=GENDER_CHOICES)
    handed = models.CharField(verbose_name='Handedness', max_length=1, 
		    	      choices=HAND_CHOICES)
    daily_usage = models.CharField(verbose_name='Daily PC Usage', max_length=10,
		  		   choices=HOUR_CHOICES)
