# api_with_restrictions/urls.py

from django.contrib import admin
from django.urls import path, include

from rest_framework.routers import DefaultRouter
from advertisements.views import AdvertisementViewSet, index

router = DefaultRouter()
router.register(r'advertisements', AdvertisementViewSet, basename='advertisement')

urlpatterns = [
    path('', index, name='index'),
    path('api/', include(router.urls)),
    path('admin/', admin.site.urls),
]
