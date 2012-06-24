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
    ('arabic', 'Arabic'),
    ('awadhi', 'Awadhi'),
    ('azerbaijani_south', 'Azerbaijani, South'),
    ('bengali', 'Bengali'),
    ('bhojpuri', 'Bhojpuri'),
    ('burmese', 'Burmese'),
    ('chinese_gan', 'Chinese, Gan'),
    ('chinese_hakka', 'Chinese, Hakka'),
    ('chinese_jinyu', 'Chinese, Jinyu'),
    ('chinese_mandarin', 'Chinese, Mandarin'),
    ('chinese_min_nan', 'Chinese, Min Nan'),
    ('chinese_wu', 'Chinese, Wu'),
    ('chinese_xiang', 'Chinese, Xiang'),
    ('chinese_yue', 'Chinese, Yue (Cantonese)'),
    ('dutch', 'Dutch'),
    ('english', 'English'),
    ('french', 'French'),
    ('german', 'German'),
    ('gujarati', 'Gujarati'),
    ('hausa', 'Hausa'),
    ('hindi', 'Hindi'),
    ('italian', 'Italian'),
    ('japanese', 'Japanese'),
    ('javanese', 'Javanese'),
    ('kannada', 'Kannada'),
    ('korean', 'Korean'),
    ('maithili', 'Maithili'),
    ('malayalam', 'Malayalam'),
    ('marathi', 'Marathi'),
    ('oriya', 'Oriya'),
    ('panjabi_western', 'Panjabi, Western'),
    ('persian', 'Persian'),
    ('polish', 'Polish'),
    ('portuguese', 'Portuguese'),
    ('romanian', 'Romanian'),
    ('russian', 'Russian'),
    ('serbo-croatian', 'Serbo-Croatian'),
    ('sindhi', 'Sindhi'),
    ('spanish', 'Spanish'),
    ('tamil', 'Tamil'),
    ('telugu', 'Telugu'),
    ('thai', 'Thai'),
    ('turkish', 'Turkish'),
    ('ukrainian', 'Ukrainian'),
    ('urdu', 'Urdu'),
    ('vietnamese', 'Vietnamese'),
    ('yoruba', 'Yoruba'),
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
