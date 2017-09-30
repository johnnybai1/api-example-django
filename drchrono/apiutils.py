import requests
from django.utils import timezone
from doctor.models import *

# Helper functions

BASE = 'https://drchrono.com/api'
# Not exhaustive
ENDPOINTS = [
    'appointments',
    'doctors',
    'offices',
    'patients',
    'patients_summary',
    'users',
    'allergies',
    'messages',
]

POST_SUCCESS = 201
PATCH_SUCCESS = 204


def get_api_url(endpoint):
    """
    Returns the appropriate API url to make requests against
    """
    if endpoint in ENDPOINTS:
        return '/'.join([BASE, endpoint])
    else:
        raise ValueError


def get_drchrono(request, url, params={}):
    """
    Makes a GET request to a drchrono API.
    """
    headers = {
        'Authorization': 'Bearer %s' % request.session['access'],
    }
    data = []
    # drchrono GET results are returned as paginated lists
    while url:
        curr_response = requests.get(url, headers=headers, params=params).json()
        data.extend(curr_response['results'])
        url = curr_response['next']
    return data


def patch_drchrono(request, url, params={}):
    """
    Makes a PATCH request to a drchrono API.
    """
    headers = {
        'Authorization': 'Bearer %s' % request.session['access'],
        'Content-type': 'application/json',
    }
    # issue patch request
    response = requests.patch(url, json=params, headers=headers)
    # return response
    return response.status_code


def post_drchrono(request, url, params={}):
    """
    Makes a POST request to a drchrono API
    """
    headers = {
        'Authorization': 'Bearer %s' % request.session['access'],
        'Content-type': 'application/json',
    }
    # issue post
    response = request.post(url, json=params, headers=headers)
    return response.status_code

"""
GETTERS
"""


def find_patient(request, first_name, last_name, ssn):
    # query params as a dict
    payload = {'first_name': first_name, 'last_name': last_name}
    # send request
    patients = get_drchrono(request, get_api_url('patients'), payload)
    # look for patient
    for p in patients:
        social = p['social_security_number']
        if social and str(ssn) == social.split('-')[2]:
            # patient found!
            return p
    # no patient exists
    return None



def find_appointment_today(request, pid, did, now):
    """
    Finds and retrieves the patient's appointment
    Consider integrating appointment time into the check
    """
    date = now.date()
    payload = {
        'patient': pid,
        'doctor': did,
        'date': date,
    }
    appts = get_drchrono(request, get_api_url('appointments'), payload)
    for a in appts:
        if a['status'] != COMPLETE:
            return a

def find_appointment_today_time(request, pid, did, time, now):
    date = now.date()
    payload = {
        'patient': pid,
        'doctor': did,
        'date': date,
    }
    appts = get_drchrono(request, get_api_url('appointments'), payload)
    for a in appts:
        sched_date, sched_time = a['scheduled_time'].split('T')
        if str(sched_time) == str(time) and str(sched_date) == str(date):
            return a


def get_todays_appointments(request, did):
    """
    Finds all checked in appointments for the doctor with id did
    """
    todays_date = timezone.localtime(timezone.now()).date()
    payload = {
        'doctor': did,
        'date': todays_date
    }
    return get_drchrono(request, get_api_url('appointments'), payload)


def get_users(request):
    return get_drchrono(request, get_api_url('users'))

"""
PATCHERS
"""


def patch_patient(request, patient, payload):
    """
    Sends patch request to patients API to update certain
    demographic data
    """
    patch_url = get_api_url('patients') + '/' + str(patient)
    status = patch_drchrono(request, patch_url, payload)
    return status


def patch_appointment_status(request, appt_id, new_status):
    """
    Updates the appointment status to a new status.
    """
    patch_url = get_api_url('appointments') + '/' + str(appt_id)
    payload = {'status': new_status}
    status = patch_drchrono(request, patch_url, payload)
    return status
