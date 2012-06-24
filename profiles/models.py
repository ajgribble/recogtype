from django.db import models
from django.contrib.auth.models import User
from userena.models import UserenaBaseProfile
from django_countries import CountryField

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

LANGUAGE_CHOICES = (
    ('Arabic', 'Arabic'),
    ('Awadhi', 'Awadhi'),
    ('Azerbaijani, South', 'Azerbaijani, South'),
    ('Bengali', 'Bengali'),
    ('Bhojpuri', 'Bhojpuri'),
    ('Burmese', 'Burmese'),
    ('Chinese, Gan', 'Chinese, Gan'),
    ('Chinese, Hakka', 'Chinese, Hakka'),
    ('Chinese, Jinyu', 'Chinese, Jinyu'),
    ('Chinese, Mandarin', 'Chinese, Mandarin'),
    ('Chinese, Min Nan', 'Chinese, Min Nan'),
    ('Chinese, Wu', 'Chinese, Wu'),
    ('Chinese, Xiang', 'Chinese, Xiang'),
    ('Chinese, Yue', 'Chinese, Yue (Cantonese)'),
    ('Dutch', 'Dutch'),
    ('English', 'English'),
    ('French', 'French'),
    ('German', 'German'),
    ('Gujarati', 'Gujarati'),
    ('Hausa', 'Hausa'),
    ('Hindi', 'Hindi'),
    ('Italian', 'Italian'),
    ('Japanese', 'Japanese'),
    ('Javanese', 'Javanese'),
    ('Kannada', 'Kannada'),
    ('Korean', 'Korean'),
    ('Maithili', 'Maithili'),
    ('Malayalam', 'Malayalam'),
    ('Marathi', 'Marathi'),
    ('Oriya', 'Oriya'),
    ('Panjabi_western', 'Panjabi, Western'),
    ('Persian', 'Persian'),
    ('Polish', 'Polish'),
    ('Portuguese', 'Portuguese'),
    ('Romanian', 'Romanian'),
    ('Russian', 'Russian'),
    ('Serbo-Croatian', 'Serbo-Croatian'),
    ('Sindhi', 'Sindhi'),
    ('Spanish', 'Spanish'),
    ('Tamil', 'Tamil'),
    ('Telugu', 'Telugu'),
    ('Thai', 'Thai'),
    ('Turkish', 'Turkish'),
    ('Ukrainian', 'Ukrainian'),
    ('Urdu', 'Urdu'),
    ('Vietnamese', 'Vietnamese'),
    ('Yoruba', 'Yoruba'),
)

class Profile(UserenaBaseProfile):
    user = models.OneToOneField(User, unique=True, verbose_name='Username', 
		    		related_name='profile')
    dob = models.DateField(verbose_name='Date of Birth', blank=True, 
                           null=True)
    sex = models.CharField(verbose_name='Sex', max_length=1, blank=True,
                           choices=GENDER_CHOICES)
    handed = models.CharField(verbose_name='Handedness', max_length=1, 
		    	              blank=True, choices=HAND_CHOICES)
    daily_usage = models.CharField(verbose_name='Daily PC Usage', max_length=10,
		  		                   blank=True, choices=HOUR_CHOICES)
    country = CountryField(verbose_name='Country of Origin', blank=True,
                           null=True)
    language = models.CharField(verbose_name='First Language', max_length=30,
                                blank=True, null=True, choices=LANGUAGE_CHOICES)
