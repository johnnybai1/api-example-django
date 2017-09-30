from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from forms import *
from drchrono.apiutils import *
from drchrono.models import *
from doctor.models import *

# Some error messages to potentially pass to html template
form_not_valid = "Please verify your check-in information and try again."
appointment_not_found = "We could not find an appointment for you today. " + \
                        "Please see receptionist for assistance."
patient_not_found = "We could not find a patient matching the information " + \
                    "supplied. Please try again or see receptionist for assistance."
appointment_update_failed = "Failed to update patient's appointment status."
demographics_update_failed = "Failed to update patient's personal information."
successful_checkin = "You have successfully checked in!"


def request_login(request, context={}):
    """
    Helper function to render login page: must choose either patient
    or doctor
    """
    context.update({'msg': 'Please log in to continue.'})
    return render(request, '/index.html', context)


def welcome_home(request, context={}):
    """
    Helper function to render kiosk home page: choose a reason for visit
    """
    context.update({'form': WelcomeForm})
    return render(request, 'kiosk/index.html', context)


def appt_checkin_home(request, context={}):
    """
    Helper function to render appointment check in page
    """
    context.update({'appt_checkin_form': AppointmentCheckinForm})
    return render(request, 'kiosk/appt_checkin.html', context)


def index(request):
    """
    For the kiosk home page. The idea here is to make sure the user arrived
    here from a successful authentication.
    The kiosk home page will let users choose why they are visiting the clinic.
    """
    if not request.user.is_authenticated():
        return request_login(request)
    # get the authorized user
    user = request.user.social_auth.get(provider='drchrono')
    request.session['id'] = int(user.uid)
    request.session['access'] = str(user.access_token)
    request.session['refresh'] = str(user.refresh_token)
    if request.method == 'POST':
        # User made a POST request to get here: clicked on "Go"
        welcome_form = WelcomeForm(request.POST)
        if welcome_form.is_valid():
            # TODO: write a method to check and redirect appropriately
            # useful when more reasons for visit are available
            if welcome_form.for_appointment():
                return appt_checkin_home(request,
                                         {'reason': 'appt_checkin'})
            if welcome_form.for_schedule():
                # TODO: Schedule appointment
                return render(request, 'kiosk/appt_schedule.html',
                              {'form': ScheduleForm})
    # Display the welcome page
    return welcome_home(request)


def appt_checkin(request):
    """
    This page will almost always handle POST requests
    If checking in: parse first name, last name, and ssn and check for
    appointment
    If successfully checked in (e.g. patient found and appointment for today
    exists): populate demographics form
    """
    now = timezone.localtime(timezone.now())
    if request.POST.get('appt_checkin_btn'):
        # User is trying to check in
        appt_checkin_form = AppointmentCheckinForm(data=request.POST)
        if appt_checkin_form.is_valid():
            # Parse fields
            patient, appointment, err = appointment_lookup(request,
                                                      appt_checkin_form,
                                                      now)
            if not err:
                data = patient_checkin(request, patient, appointment, now)
                return appt_checkin_home(request, data)
            return err
    if request.POST.get('info_confirm_btn'):
        # Patient confirmed their demographic info. Lets update the fields
        demographics_form = DemographicsForm(request.POST)
        if demographics_form.is_valid():
            # update patient demographics
            fields = demographics_form.fields
            update = {k: demographics_form.cleaned_data[k] for k in fields}
            response = patch_patient(request, request.session['patient_id'], update)
            del request.session['patient_id']
        message_form = MessageForm(request.POST)
        if message_form.is_valid():
            # Update the appointment message
            message = message_form.cleaned_data['message']
            appt = Appointment.objects.get(pk=request.session['appointment_id'])
            appt.message = message
            appt.save()
            del request.session['appointment_id']
        print 'returning'
        return welcome_home(request, {'success': successful_checkin})
    return appt_checkin_home(request)


def appointment_lookup(request, form, now):
    """
    Parses the appointment check in form for first name, last name, and last 4
    digits of SSN. Returns a tuple (patient, appointment, error)
    If a patient with an appointment today is found, error is False. If any
    errors occured in the process, error will be an HttpResponse.
    """
    if form.is_valid():
        # Parse fields
        first_name = form.cleaned_data['first_name']
        last_name = form.cleaned_data['last_name']
        appt_time = form.cleaned_data['appt_time']
        ssn = form.cleaned_data['ssn']
        # Look for patient
        patient = find_patient(request, first_name, last_name, ssn)
        if patient:
            appointment = find_appointment_today_time(request,
                                                  patient['id'],
                                                  patient['doctor'],
                                                  appt_time,
                                                  now)
            if appointment:
                # Found the appointment
                request.session['patient_id'] = patient['id']
                return patient, appointment, False
            else:
                # No appointment. Return to check in page with msg
                return None, None, appt_checkin_home(request,
                                    {'msg': appointment_not_found})
        else:
            # No patient. Return to check in page with msg
            return None, None, appt_checkin_home(request,
                                     {'msg': patient_not_found})
    else:
        # Form not valid. Return to check in page with msg
        return None, None, appt_checkin_home(request,
                                {'msg': form_not_valid})


def patient_checkin(request, patient, appointment, now):
    """
    This function is called only if an appointment is successfully found.
    We return a context dictionary to render our html template appropriately.
    """
    data = {}
    appt_obj, created = Appointment.objects.get_or_create(
        id=appointment['id'],
        first_name=patient['first_name'],
        last_name=patient['last_name'],
        scheduled_time=appointment['scheduled_time'].split('T')[1],
    )
    if created:
        # Appointment did not exist in our database, update fields
        # We do not want to update checkin_date and _time unless we are sure
        # they havent been recorded yet. (Don't want to mess up our stats!)
        appt_obj.checkin_date = now.date()
        appt_obj.checkin_time = now.time()
        response = patch_appointment_status(request,
                                            appointment['id'],
                                            CHECKED_IN)
        appt_obj.save()
        # TODO: Check and handle failure to patch
    else:
        # Object was got, patient already checked in
        data['status'] = CHECKED_IN
    # Parses our patient object to build the form
    data['first_name'] = patient['first_name']
    # Populate demographic form with patient dict
    data['demographics_form'] = DemographicsForm(patient)
    # Populate message form with whatever the patient had written before
    data['message_form'] = MessageForm({'message': appt_obj.message})
    request.session['appointment_id'] = appointment['id']
    return data


def appt_schedule(request):
    if request.POST.get('schedule_confirm_btn'):
        # User hit confirm
        form = ScheduleForm(request.POST)
        if form.is_valid():
            time = form.cleaned_data['time']
    return HttpResponse("UNDER DEVELOPMENT")