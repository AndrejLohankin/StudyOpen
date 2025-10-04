from django.urls import path
from calculator.views import calculate_view

urlpatterns = [
    path('<str:dish>/', calculate_view, name='dish'),
]