from django.db import models
from django import forms
from drchrono.models import Doctor

# Create your models here.
"""
CHOICE FIELD CREATION
ModelForm style for choice fields
https://docs.djangoproject.com/en/1.11/topics/forms/modelforms/
"""
# Generally applicable choices
BLANK = 'blank'
DECLINED = 'declined'
OTHER = 'other'
# Reason for visiting
APPOINTMENT = 'appt_checkin'
SCHEDULE = 'appt_schedule'
REASON_FOR_VISIT_CHOICES = [
    (APPOINTMENT, 'I have an appointment'),
    (SCHEDULE, 'I want to schedule an appointment')
]
# Gender
MALE = 'Male'
FEMALE = 'Female'
GENDER_CHOICES = [
    (MALE, 'Male'),
    (FEMALE, 'Female'),
    (OTHER, 'Other'),
    (DECLINED, 'Declined to specify'),
]
# Race
INDIAN = 'indian'
ASIAN = 'asian'
BLACK = 'black'
HAWAIIAN = 'hawaiian'
WHITE = 'white'
RACE_CHOICES = [
    (BLANK, 'None'),
    (INDIAN, 'American Indian or Alaska Native'),
    (ASIAN, 'Asian'),
    (BLACK, 'Black or African American'),
    (WHITE, 'White'),
    (DECLINED, 'Declined to specify'),
]
# Ethnicity
HISPANIC = 'hispanic'
NOT_HISPANIC = 'not_hispanic'
ETHNICITY_CHOICES = [
    (BLANK, 'None'),
    (HISPANIC, 'Hispanic or Latino'),
    (NOT_HISPANIC, 'Not Hispanic or Latino'),
    (DECLINED, 'Declined to specify'),
]


class Reason(models.Model):
    """
    Choices for reason to visit on welcome page
    """
    reason_for_visit = models.CharField(max_length=30,
                                        choices=REASON_FOR_VISIT_CHOICES,
                                        default=APPOINTMENT)


class AppointmentCheckIn(models.Model):
    """
    Fields to allow patient to check in
    """
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    ssn = models.IntegerField()
    appt_time = models.CharField(max_length=10,
                                 help_text='hh:mm AM/PM')


class Demographics(models.Model):
    """
    Fields to present certain patient info to the patient
    """
    date_of_birth = models.CharField(max_length=10,
                                     default=BLANK,
                                     help_text='yyyy-mm-dd')
    address = models.CharField(max_length=200,
                               default=BLANK,
                               blank=True)
    zip_code = models.IntegerField(default=-1,
                                   blank=True)
    city = models.CharField(max_length=100,
                            default=BLANK,
                            blank=True)
    emergency_contact_name = models.CharField(max_length=100,
                                      default=BLANK,
                                      blank=True)
    emergency_contact_phone = models.CharField(max_length=20,
                                       default=BLANK,
                                       blank=True)
    emergency_contact_relation = models.CharField(max_length=50,
                                          default=BLANK,
                                          blank=True)
    gender = models.CharField(max_length=10,
                              choices=GENDER_CHOICES,
                              default=BLANK,
                              blank=True)
    race = models.CharField(max_length=50,
                            choices=RACE_CHOICES,
                            default=BLANK,
                            blank=True)
    ethnicity = models.CharField(max_length=50,
                                 choices=ETHNICITY_CHOICES,
                                 default=BLANK,
                                 blank=True)


class Message(models.Model):
    """
    Just a simple text area for patients to give any extra info to their doctor
    """
    message = models.TextField(max_length=500,
                               default='',
                               blank=True)


class Schedule(models.Model):
    """
    Basic template to schedule an appointment
    """
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=5)
    date_of_birth = models.CharField(max_length=10,
                                     help_text='yyyy-mm-dd')
    time = models.CharField(max_length=10,
                            help_text='HH:MM AM/PM',
                            verbose_name='Appointment Time')