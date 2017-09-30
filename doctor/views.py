from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.views.generic import DetailView
from myutils import *
from models import *
# Create your views here


err_patch = "There was a problem updating patient status."


def request_login(request, context={}):
    context.update({'msg': 'Please log in to continue.'})
    return render(request, 'index.html', context)


def index(request, context={}):
    """
    Doctor home page
    Give some summary info about his day: e.g. number of patients left to see
    """
    if not request.user.is_authenticated():
        # Force user to login
        return request_login(request)
    data = {}
    if not request.session.get('is_doctor'):
        # We make sure this user is a doctor first
        user = request.user.social_auth.get(provider='drchrono')
        user_id = int(user.uid)
        request.session['doctorid'] = user_id
        request.session['access'] = str(user.access_token)
        request.session['refresh'] = str(user.refresh_token)
        # Get list of users from drchrono api
        drchrono_users = get_users(request)
        for u in drchrono_users:
            if u['id'] == user_id and u['is_doctor']:
                # Set this to true
                request.session['is_doctor'] = True
                # Get this doctor's name
                doctor = get_drchrono(request,
                                      get_api_url('doctors'),
                                      {'id': u['id']})[0]
                request.session['first_name'] = doctor['first_name']
                request.session['last_name'] = doctor['last_name']
                Doctor.objects.get_or_create(id=user_id,
                                             first_name=doctor['first_name'],
                                             last_name=doctor['last_name'])
    if request.session.get('is_doctor'):
        # Doctor home view will display some information about today
        # Lets tell the doctor how many appointments he has left today
        remaining = get_remaining_appointments(request)
        # TODO: Get doctor's next scheduled appt.
        data['first_name'] = request.session['first_name']
        data['last_name'] = request.session['last_name']
        data['remaining'] = len(remaining)
        context.update(data)
        return render(request, 'doctor/index.html', data)
    # Not a doctor / not logged in
    return request_login(request)


def appointments(request):
    """
    Appointments page. Show a list of checked in patients and have a running
    timer of the average wait time of patients. Show a list of IN_SESSION and
    COMPLETE patients as well to revisit their patient page
    """
    now = timezone.localtime(timezone.now())
    data = {}
    tables = {}
    rows = []
    seen = Appointment.objects.filter(seen_time__isnull=False).filter(
        checkin_date__iexact=now.date())
    # Today's COMPLETE patients
    complete = seen.filter(finish_time__isnull=False)
    for a in complete:
        d = {}
        d['id'] = a.id
        d['name'] = a.first_name + ' ' + a.last_name
        h, m, s = to_hms(get_waiting_time(a, now.time()))
        wait_time = "" + str(h) + ":" + str(m) + ":" + str(s)
        d['wait_time'] = wait_time
        rows.append(d)
    tables['Completed'] = rows
    rows = []
    # Today's IN_SESSION patients
    in_session = seen.filter(finish_time__isnull=True)
    for a in in_session:
        d = {}
        d['id'] = a.id
        d['name'] = a.first_name + ' ' + a.last_name
        h, m, s = to_hms(get_waiting_time(a, now.time()))
        wait_time = "" + str(h) + ":" + str(m) + ":" + str(s)
        d['wait_time'] = wait_time
        rows.append(d)
    tables['In Session'] = rows
    data['tables'] = tables
    return render(request, 'doctor/appointments.html', data)


def refresh_checkins(request):
    """
    Code to query our database to update check in table
    """
    if request.method == 'GET':
        data = {}
        # today's checked in appointments
        data['appointments'] = get_checked_in_appointments()
    return JsonResponse(data) # JsonResponse; returned to $.ajax


def refresh_wait(request):
    """
    Code to query our database to update average
    """
    now = timezone.localtime(timezone.now())
    appointments = Appointment.objects.filter(
        checkin_date__iexact=now.date())
    count = appointments.count()
    total_wait = sum([get_waiting_time(appt, now.time()) for appt in appointments])
    if count == 0:
        average_seconds = 0
    else:
        average_seconds = total_wait / count
    h, m, s = to_hms(average_seconds)
    data = {'hours': h,
            'minutes': m,
            'seconds': s}
    return JsonResponse(data) # JsonResponse; returned to $.ajax


class PatientDetails(DetailView):
    model = Appointment
    template_name = 'doctor/patient.html'

    def dispatch(self, request, *args, **kwargs):
        this = super(PatientDetails, self).dispatch(request, *args, **kwargs)
        if request.GET.get('confirm_see_patient'):
            # We arrived here because doctor chose to see this patient
            # Update patient status and patch
            err = self.see_patient(request)
            if err:
                return index(request, {'msg': err})
        return this

    def get_context_data(self, **kwargs):
        context = super(PatientDetails, self).get_context_data()
        # Supply wait time
        now = timezone.localtime(timezone.now())
        h, m, s = to_hms(get_waiting_time(self.get_object(),
                                                now.time()))
        context['hours'] = h
        context['minutes'] = m
        context['seconds'] = s
        # Make API call to get more info
        appts = get_drchrono(self.request, get_api_url('appointments'),
                            {'doctor': self.request.session['doctorid'],
                             'date': now.date()}
                            )
        for a in appts:
            if a['id'] == context['appointment'].id:
                appt = a
        # Provide notes
        if appt.get('reason'):
            context['reason'] = appt.get('reason')
        else:
            context['reason'] = 'None Specified'
        context['notes'] = appt.get('notes')
        context['message'] = self.get_object().message
        # Provide reason
        return context

    def get_object(self):
        obj = get_object_or_404(Appointment, pk=self.kwargs.get('appointment_id'))
        return obj

    def get_queryset(self):
        return Appointment.objects.filter(pk=self.kwargs.get('appointment_id'))

    def see_patient(self, request):
        """
        Update + patch appointment to reflect that patient is being seen
        Returns None if succesfully patched, otherwise an error message
        """
        appt = self.get_object() # Appointment object
        appt.status = IN_SESSION
        appt.seen_time = timezone.localtime(timezone.now()).time()
        response = patch_appointment_status(request, appt.id, IN_SESSION)
        if response:
            appt.save()
            return None
        return err_patch


def patient_done(request, appointment_id):
    """
    Called when "confirm" is pressed on Patient DetailView modal (activated by
    'Patient Done' button)
    :return:
    """
    appt_obj = Appointment.objects.get(pk=appointment_id)
    if appt_obj.finish_time is None:
        # we have not set this appointment as complete yet
        appt_obj.finish_time = timezone.localtime(timezone.now()).time()
        response = patch_appointment_status(request, appointment_id, COMPLETE)
        if response != 204:
            return index(request, {'msg': err_patch})
    appt_obj.save()
    # TODO: Create a notes log to allow doctor to view history and revert
    return HttpResponseRedirect(reverse('doctor:appointments'))


def appointment_stats(request):
    """
    Lets calculate some statistics for the doctors
    We'll assume the doctor's been using the web app, thus all of the past
    appointments with statuses are stored.
    """
    # TODO: Consider/Look into Django cache framework
    # Default is to load up yesterday's stats
    data = {}
    if request.GET.get('lookback'):
        data['lookback'] = request.GET.get('lookback')
        appointments = get_appointments_word(request.GET.get('lookback'))
    else:
        data['lookback'] = 'yesterday'
        appointments = get_appointments_word('yesterday')
    data.update(get_appointment_stats(appointments))
    return render(request, 'doctor/stats.html', data)
