from django.db import models
from drchrono.models import Appointment
# Create your models here.

BLANK = ''
ARRIVED = 'Arrived'
CANCELLED = 'Cancelled'
CHECKED_IN = 'Checked In'
COMPLETE = 'Complete'
CONFIRMED = 'Confirmed'
IN_SESSION = 'In Session'
NO_SHOW = 'No Show'
NOT_CONFIRMED = 'Not Confirmed'
RESCHEDULED = 'Rescheduled'
APPT_STATUS_CHOICES = [
    (BLANK, BLANK),
    (ARRIVED, ARRIVED),
    (CANCELLED, CANCELLED),
    (CHECKED_IN, CHECKED_IN),
    (COMPLETE, COMPLETE),
    (CONFIRMED, CONFIRMED),
    (IN_SESSION, IN_SESSION),
    (NO_SHOW, NO_SHOW),
    (NOT_CONFIRMED, NOT_CONFIRMED),
    (RESCHEDULED, RESCHEDULED)
]


class AppointmentStatus(models.Model):
    status = models.CharField(max_length=20,
                              choices=APPT_STATUS_CHOICES,
                              default=BLANK)


class PatientInfo(models.Model):
    name = models.CharField(max_length=60)
    checkin_time = models.CharField(max_length=20)
    wait_time = models.CharField(max_length=8)
    reason = models.CharField(max_length=100)
    message = models.TextField(max_length=500,
                               blank=True,
                               default='')