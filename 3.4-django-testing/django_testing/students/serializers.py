from rest_framework import serializers
from django.conf import settings
from students.models import Course, Student

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ("id", "name", "students")

    def validate_students(self, value):
        if len(value) > getattr(settings, 'MAX_STUDENTS_PER_COURSE', 20):
            raise serializers.ValidationError('Превышено максимальное количество студентов на курсе.')
        return value