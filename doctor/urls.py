from django.conf.urls import url, include
from django.views.generic import TemplateView
from . import views

app_name = 'doctor'
urlpatterns = [
    # /doctor/
    url(r'^$', views.index, name='index'),
    # /doctor/appointments
    url(r'^appointments/$', views.appointments, name='appointments'),
    url(r'^appointments/refresh_table/$', views.refresh_checkins,
        name='refresh_checkins'),
    url(r'^appointments/refresh_wait/$', views.refresh_wait,
        name='refresh_wait'),
    url(r'^patient/(?P<appointment_id>[0-9]+)/$', views.PatientDetails.as_view(),
        name='see_patient'),
    url(r'patient/(?P<appointment_id>[0-9]+)/done/$', views.patient_done,
        name='patient_done'),
    url(r'^stats/$', views.appointment_stats, name='stats'),
]
