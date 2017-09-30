from django.db import models

# Create your models here.

"""
We'll keep database models (as opposed to form models) here since multiple 
applications may want to access them
"""

class Appointment(models.Model):
    """
    Used to keep track of stats regarding patient appointments
    This will let us produce various stats, including average wait time
    """
    # Appointment id is obtained from appointments api
    id = models.CharField(max_length=30,
                          primary_key=True)
    # Patient's first name
    first_name = models.CharField(max_length=30)
    # Patient's last name
    last_name = models.CharField(max_length=30)
    # What day did this patient check in?
    checkin_date = models.DateField(blank=True,
                                    null=True)
    # When is this patient's scheduled appointment?
    scheduled_time = models.TimeField(blank=True,
                                      null=True)
    # When did this person finish checking in?
    checkin_time = models.TimeField(blank=True,
                                    null=True)
    # When did the doctor start session with patient?
    # This time is set when doctor marks patient's status as IN_SESSION
    seen_time = models.TimeField(blank=True,
                                 null=True)
    # When did the session end?
    # This time is set when doctor marks patient's status as COMPLETE
    finish_time = models.TimeField(blank=True,
                                   null=True)
    # Message for doctor
    message = models.TextField(max_length=500,
                               blank=True,
                               default='')


class Doctor(models.Model):
    """
    Used to keep track of doctors at this clinic. Easier to populate choices
    for doctors when scheduling an appointment
    """
    id = models.CharField(max_length=30,
                          primary_key=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)