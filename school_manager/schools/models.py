from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Person(models.Model):
    user = models.OneToOneField(User)
    first_name = models.CharField(max_length=80)
    last_name = models.CharField(max_length=80)

class School(models.Model):
    name = models.CharField(max_length=80)

class Location(models.Model):
    school = models.ForeignKey(School)
    name = models.CharField(max_length=50)
    managers = models.ManyToManyField(Person)
    address_1 = models.CharField(max_length=50)
    address_2 = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    state_province = models.CharField(max_length=4)
    zip_postal_code = models.CharField(max_length=10)
    country = models.CharField(max_length=2)

class Course(models.Model):
    location = models.ForeignKey(Location)
    name = models.CharField(max_length=50)
    instructors = models.ManyToManyField(Person, related_name="instructors")
    students = models.ManyToManyField(Person, related_name="students")

class Session(models.Model):
    course = models.ForeignKey(Course)
    students = models.ManyToManyField(Person)
    datetime = models.DateTimeField()

	
	
