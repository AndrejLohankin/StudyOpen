from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('sensors/', views.sensors_list, name='sensors-list'),
    path('sensors/<int:pk>/', views.sensor_detail, name='sensor-detail'),
    path('sensors/<int:pk>/update/', views.sensor_update, name='sensor-update'),
    path('measurements/', views.add_measurement, name='add-measurement'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)