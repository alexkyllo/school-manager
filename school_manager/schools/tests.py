from django.test import TestCase
from schools.models import *

# Create your tests here.

class NewSchoolLocation(TestCase):
	def setUp(self):
		cool_school = School.objects.create(name="A Cool School")
		Location.objects.create(school=cool_school, name="Kirkland")
	
	def testSchoolHasLocation(self):
		cool_school = School.objects.get(name="A Cool School")
		location = Location.objects.get(name="Kirkland")
		self.assertEqual(location.school, cool_school)
