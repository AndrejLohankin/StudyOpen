from django.db import models
from django.core.validators import MaxValueValidator, ValidationError
from django.conf import settings


class Student(models.Model):

    name = models.TextField()

    birth_date = models.DateField(
        null=True,
    )


class Course(models.Model):

    name = models.TextField()

    students = models.ManyToManyField(
        Student,
        blank=True,
    )
