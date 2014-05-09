from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class Person(models.Model):
    user = models.OneToOneField(User)
    first_name = models.CharField(max_length=80)
    last_name = models.CharField(max_length=80)

    def __str__(self):
        return self.first_name + " " + self.last_name

class School(models.Model):
    name = models.CharField(max_length=80)

    def __str__(self):
        return self.name

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

    def __str__(self):
        return self.name    

class Course(models.Model):
    location = models.ForeignKey(Location)
    name = models.CharField(max_length=50)
    instructors = models.ManyToManyField(Person, related_name="instructors")
    students = models.ManyToManyField(Person, related_name="students")

    def __str__(self):
        return self.name

class Session(models.Model):
    course = models.ForeignKey(Course)
    students = models.ManyToManyField(Person)
    startdatetime = models.DateTimeField()
    enddatetime = models.DateTimeField()


    def __str__(self):
        startdatetime = timezone.localtime(self.startdatetime)
        return self.course.name + " on " + startdatetime.strftime("%B")

	
	
