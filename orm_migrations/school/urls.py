from django.urls import path

from school.views import StudentsListView

urlpatterns = [
    path('', StudentsListView.as_view(), name='students'),
]
