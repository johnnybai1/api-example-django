from django import forms
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from datetime import datetime
from django.utils import timezone
from drchrono.models import Doctor
import time

from .models import *

# Forms to follow Django's ModelForm design
# Note: can do fields = '__all__' to select all fields
# Alternatively, can exclude = []


class WelcomeForm(ModelForm):
    class Meta:
        model = Reason
        fields = [
            'reason_for_visit',
        ]

    def for_appointment(self):
        return self.cleaned_data['reason_for_visit'] == APPOINTMENT

    def for_schedule(self):
        return self.cleaned_data['reason_for_visit'] == SCHEDULE


class AppointmentCheckinForm(ModelForm):
    class Meta:
        model = AppointmentCheckIn
        fields = [
            'first_name',
            'last_name',
            'ssn',
            'appt_time',
        ]
        widgets = {
            # hide ssn
            'ssn': forms.PasswordInput(),
        }

    def clean_first_name(self):
        data = self.cleaned_data['first_name']
        if not data.isalpha():
            raise ValidationError(_('Invalid first name - must contain only letters'))
        return data

    def clean_last_name(self):
        data = self.cleaned_data['last_name']
        if not data.isalpha():
            raise ValidationError(_('Invalid last name - must contain only letters'))
        return data

    def clean_appt_time(self):
        time = self.cleaned_data['appt_time']
        # The user must specify the time as HH:MM AM/PM or H:MM AM/PM
        squish = str(time).replace(' ', '')
        if len(squish) == 6:
            # H:MMAM
            squish = '0' + squish
        if len(squish) != 7:
            raise ValidationError(_('Must input time as HH:MM AM/PM.'))
        try:
            time = datetime.strptime(squish, '%I:%M%p')
            return time.strftime('%H:%M') + ':00' # 24 hour format to compare to scheduled_time
        except ValueError:
            raise ValidationError(_('Must input time as HH:MM AM/PM'))

    def clean_ssn(self):
        data = self.cleaned_data['ssn']
        # TODO: account for ssn's with leading 0's
        if data < 1000 or data > 9999:
            raise ValidationError(_('Must enter the last 4 digits of your SSN'))
        return data


class DemographicsForm(ModelForm):
    class Meta:
        model = Demographics
        fields = [
            'date_of_birth',
            'address',
            'zip_code',
            'city',
            'emergency_contact_name',
            'emergency_contact_phone',
            'emergency_contact_relation',
            'gender',
            'race',
            'ethnicity',
        ]

    def clean_date_of_birth(self):
        data = self.cleaned_data['date_of_birth']
        # expect yyyy-mm-dd
        try:
            date = datetime.strptime(data, '%Y-%m-%d').date()
            if date > timezone.localtime(timezone.now()).date():
                raise ValidationError(_('Birthday cannot be in the future!'),
                                      code='future_bday')
            return data
        except ValueError:
            raise ValidationError(_('Check format: yyyy-mm-dd'),
                                  code='date_format_error')

    def clean_address(self):
        return self.cleaned_data['address']

    def clean_zip_code(self):
        data = self.cleaned_data['zip_code']
        try:
            val = int(data)
            if val != 1 and val < 10000 or val > 99999:
                raise ValidationError(_('Zip code must be 5 digits'),
                                  code='invalid_zip')
            return data
        except ValueError:
            raise ValidationError(_('Zip code must be numeric'),
                                  code='zip_format_error')

    def clean_city(self):
        return self.cleaned_data['city']

    def clean_emergency_contact_name(self):
        return self.cleaned_data['emergency_contact_name']

    def clean_emergency_contact_number(self):
        data = self.cleaned_data['emergency_contact_number']
        try:
            val = int(data)
            return data
        except ValueError:
            raise ValidationError(_('Phone number must be digits only'),
                                  code='invalid_number')

    def clean_emergency_contact_relation(self):
        return self.cleaned_data['emergency_contact_relation']

    def clean_gender(self):
        return self.cleaned_data['gender']

    def clean_race(self):
        return self.cleaned_data['race']

    def clean_ethnicity(self):
        return self.cleaned_data['ethnicity']


class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ['message']


class DoctorChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return 'Dr. %s %s' % (obj.first_name, obj.last_name)


class ScheduleForm(ModelForm):
    class Meta:
        model = Schedule
        fields = [
            'first_name',
            'last_name',
            'date_of_birth',
            'time',
        ]

        def clean_time(self):
            time = self.cleaned_data['time']
            # The user must specify the time as HH:MM AM/PM or H:MM AM/PM
            squish = str(time).replace(' ', '')
            if len(squish) == 6:
                # H:MMAM
                squish = '0' + squish
            if len(squish) != 7:
                raise ValidationError(_('Must input time as HH:MM AM/PM.'))
            try:
                time = datetime.strptime(squish, '%I:%M%p')
                return time.strftime(
                    '%H:%M') + ':00'  # 24 hour format to compare to scheduled_time
            except ValueError:
                raise ValidationError(_('Must input time as HH:MM AM/PM'))
    doctor = DoctorChoiceField(queryset=Doctor.objects.all(),
                                    empty_label=None)

