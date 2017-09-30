from django.conf.urls import url
import drchrono
from . import views

app_name = 'kiosk'
urlpatterns = [
    # /kiosk/
    url(r'^$', views.index, name='index'),
    # /kiosk/appt_checkin
    url(r'^appt_checkin/$', views.appt_checkin, name='appt_checkin'),
    # /kiosk/appt_schedule
    url(r'^schedule/$', views.appt_schedule, name='appt_schedule')
]