from drchrono.apiutils import *
from drchrono.models import *
from models import *
from datetime import datetime, timedelta

APPT_TIME_FMT = '%H:%M:%S'
days_of_week = ['Monday', 'Tuesday', 'Wednesday',
                'Thursday', 'Friday', 'Saturday', 'Sunday']


def get_remaining_appointments(request):
    # Get today's appointments via API call
    appts = get_todays_appointments(request, request.session['doctorid'])
    # Appointments with status not marked as complete
    return [a for a in appts if a['status'] != COMPLETE]


def get_checked_in_appointments():
    """
    Return a list of today's checked in appointments
    """
    now = timezone.localtime(timezone.now())
    todays_appts = []
    set = Appointment.objects.filter(checkin_date__iexact=now.date(),
                                     seen_time__isnull=True)
    if set:
        todays_appts = []
        for a in set:
            data = {}
            data['id'] = a.id
            data['first_name'] = a.first_name
            data['last_name'] = a.last_name
            data['checkin_time'] = a.checkin_time
            wait_time_seconds = get_waiting_time(a, now.time())
            h, m, s = to_hms(wait_time_seconds)
            data['hours'] = h
            data['minutes'] = m
            data['seconds'] = s
            todays_appts.append(data)
    return todays_appts
    # return render(request, 'doctor/todays_appts.html',
    #               { 'checked_in_patients': todays_appts})


def get_waiting_time(appointment, curr_time):
    """
    Calculates how much time a patient has been waiting
    :param appointment: The Appointment object (drchrono.models.Appointment)
    :param curr_time: a datetime object (time only)
    :return: time spent waiting in seconds
    """
    today = datetime.today().date()
    checkin_time = datetime.combine(today, appointment.checkin_time)
    seen_time = appointment.seen_time
    if seen_time:
        # patient has already been seen
        wait = datetime.combine(today, seen_time) - checkin_time
    else:
        # patient is still waiting
        wait = datetime.combine(today, curr_time) - checkin_time
    return wait.seconds if wait.seconds > 0 else 0


def get_adjusted_waiting_time(appointment):
    """
    Calculates how long this patient has been waiting PAST their scheduled
    appointment
    """
    today = datetime.today().date()
    scheduled_time = datetime.combine(today, appointment.scheduled_time)
    seen_time = datetime.combine(today, appointment.seen_time)
    wait = seen_time - scheduled_time
    return wait.seconds if wait.seconds > 0 else 0



def to_hms(seconds):
    """
    Calculations to convert seconds to hours, minutes, and seconds
    """
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    return int(h), int(m), int(s)


def get_appointments(first_date, last_date):
    """
    Query Appointment db for all appointments between two dates
    [first_date, last_date] (inclusive)
    :param first_date:
    :param last_date:
    :return:
    """
    return Appointment.objects.filter(checkin_date__lte=last_date,
                                      checkin_date__gte=first_date)


def get_appointments_word(str):
    """
    Gets appointments within a certain look-back period. Will also parse the
    query set to determine day of week (e.g. mon, tues, .. sun)
    :param str:
    :return:
    """
    yesterday = timezone.localtime(timezone.now()) - timedelta(days=1)
    start = ''
    if str =='yesterday':
        start = yesterday
    if str == 'week':
        start = yesterday - timedelta(days=7)
    elif str == '30_days':
        start = yesterday - timedelta(days=30)
    elif str == '180_days':
        start = yesterday - timedelta(days=180)
    if start == '':
        raise ValueError(str + ' is not a valid choice!')
    return get_appointments(start.date(), yesterday.date())


def get_appointment_stats(appointments):
    """
    Calculates some fun stats for the appointments queryset provided
    Returns a dictionary with the following measures. All time is recorded in
    seconds.

    count: number of appointments
    total_wait: total time patients had to wait
    adj_wait: total time patients had to wait past their scheduled time
    by_day: total wait time of patients for each day
    by_day_csv: by_day as a csv
    adj_by_day: adjusted wait time of patients for each day
    adj_by_day_csv: adj_by_day as a csv
    avg_wait: average wait time of patients
    avg_by_day: average wait time of patients for each day
    avg_by_day_csv: avg_by_day as csv
    adj_avg_by_day: average adjusted wait time of patients for each day
    adj_avg_by_day_list: avg_by_day as a csv
    """
    num_appointments = appointments.count()
    total_wait_seconds = 0
    adj_total_wait = 0
    # total and/or average waits by day of week
    by_day = { k : 0 for k in days_of_week }
    adj_by_day = { k : 0 for k in days_of_week }
    for a in appointments:
        # it does not matter what time we put in since we're dealing with
        # finished patients
        curr_wait = get_waiting_time(a, timezone.now().time())
        adj_wait = get_adjusted_waiting_time(a)
        total_wait_seconds += curr_wait
        adj_total_wait += adj_wait
        day = a.checkin_date.weekday()
        by_day[days_of_week[day]] += curr_wait
        adj_by_day[days_of_week[day]] += adj_wait
        data = {'count': num_appointments,
            'total_wait': total_wait_seconds,
            'adj_wait': adj_total_wait,
            'by_day':by_day,
            'adj_by_day': adj_by_day,
            'avg_wait': int(round(total_wait_seconds/num_appointments)),
            'avg_by_day': {k: int(round(by_day[k]/num_appointments)) for k in days_of_week},
            'adj_avg_by_day' : {k: int(round(adj_by_day[k]/num_appointments)) for k in days_of_week}
        }
    # We want h,m,s still to display summary sentence to doctor
    h, m, s = to_hms(data.get('avg_wait'))
    data['h'] = str(h)
    data['m'] = str(m)
    data['s'] = str(s)
    # fix up by_day
    by_day = data['by_day']
    data['by_day'] = get_by_day_times(by_day)
    data['by_day_csv'] = get_by_day_csv(by_day)
    # fix up adj_by_day
    adj_by_day = data['adj_by_day']
    data['adj_by_day'] = get_by_day_times(adj_by_day)
    data['adj_by_day_csv'] = get_by_day_csv(adj_by_day)
    # fix up avg_by_day
    avg_by_day = data['avg_by_day']
    data['avg_by_day'] = get_by_day_times(avg_by_day)
    data['avg_by_day_csv'] = get_by_day_csv(avg_by_day)
    # fix up adj_avg_by_day
    adj_avg_by_day = data['adj_avg_by_day']
    data['adj_avg_by_day'] = get_by_day_times(adj_avg_by_day)
    data['adj_avg_by_day_csv'] = get_by_day_csv(adj_avg_by_day)
    return data


def get_by_day_csv(by_day):
    # Converts a wait time by day (seconds) dictionary to csv (minutes)
    # index 0 is Monday, index 6 is Sunday
    return ",".join([str(int(by_day[k]/60)) for k in days_of_week])


def get_by_day_times(by_day):
    # Converts a wait time by day dictionary values from seconds to time
    return {k: seconds_to_time(by_day[k]) for k in by_day}


def seconds_to_time(seconds):
    sb = ''
    h, m, s = to_hms(seconds)
    if h < 10:
        sb += '0'
    sb += str(h) + ':'
    if m < 10:
        sb += '0'
    sb += str(m) + ':'
    if s < 10:
        sb += '0'
    sb += str(s)
    return sb
