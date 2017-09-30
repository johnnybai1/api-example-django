from django.conf.urls import include, url
from django.views.generic import TemplateView
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
import views

app_name='drchrono'

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', TemplateView.as_view(template_name='index.html'), name='index'),
    url(r'', include('social.apps.django_app.urls', namespace='social')),
    url(r'^kiosk/', include('kiosk.urls', namespace='kiosk')),
    url(r'^doctor/', include('doctor.urls', namespace='doctor')),
    url(r'^logout/$', views.logout, name='logout')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)