from django.forms import ModelForm
from models import PatientInfo

class PatientInfoForm(ModelForm):
    class Meta:
        model = PatientInfo
        fields = [
            'name',
            'checkin_time',
            'wait_time',
            'reason',
            'message',
        ]