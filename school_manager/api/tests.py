from django.test import TestCase
from schools.models import *
from schools.views import SchoolList
from django.contrib.auth.models import Group
from datetime import datetime, timedelta
from django.utils.timezone import utc
from django.test.client import RequestFactory, Client

class TestSchoolViews(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.client = Client()
        self.valid_user = User.objects.create_user(username='alex', first_name="Alex", last_name="Kyllo", password="42")
        managers_group = Group.objects.create(name="Managers")
        self.valid_user.groups.add(managers_group)
        self.invalid_user = User.objects.create_user(username='root', first_name="root", last_name="root")

    def testValidUserCanViewSchoolsList(self):
        request = self.factory.get('/api/schools/')
        request.user = self.valid_user
        response = SchoolList.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def testInvalidUserCannotViewSchoolsList(self):
        request = self.factory.get('/api/schools/')
        request.user = self.invalid_user
        response = SchoolList.as_view()(request)
        self.assertFalse(response.context_data['object_list'])
        #self.assertRedirects(response, '/accounts/login/?next=/schools/', status_code=302, target_status_code=200)

    def testValidUserCanCreateSchool(self):
        self.client.login(username='alex', password='42')
        self.client.post('/api/schools/', {"name": "Testing School"})
        testing_school = School.objects.get(name='Testing School')
        self.assertTrue(testing_school)

    def testInvalidUserCannotCreateSchool(self):
        self.client.login(username='root', password='password')
        self.client.post('/api/schools/', {'name': 'Fake Testing School'})
        try: 
            School.objects.get(name='Fake Testing School')
        except:
            self.assertTrue(True)

    def testValidUserCanViewSchoolDetail(self):
        request = self.factory.get('/api/schools/1/')
        request.user = self.valid_user
        response = SchoolList.as_view()(request)
        self.assertEqual(response.status_code, 200)

class TestAccounts(TestCase):
    def setUp(self):
        self.client = Client()
        Group.objects.create(name="Managers")
        User.objects.create_user(username='dawn', first_name='Dawn', last_name='Kyllo', password='ruby')
        
    def testInvalidUserCannotLogIn(self):
        self.assertEqual(self.client.login(username='root', password='password'), False)

    def testValidUserCanLogIn(self):
        self.assertTrue(self.client.login(username='dawn', password='ruby'))

class TestStudentViews(TestCase):
    fixtures = ['users.json', 'groups.json', 'schools.json']
    def setUp(self):
        self.client = Client()

    def test_managers_can_view_school_students_list(self):
        self.client.login(username='kyllo', password='password')
        response = self.client.get('/api/schools/1/students/')
        self.assertContains(response, 'Ruby Dog', status_code=200)

    def test_managers_can_view_school_students_detail(self):
        self.client.login(username='kyllo', password='password')
        response = self.client.get('/api/users/ruby/')
        self.assertContains(response, 'Ruby Dog', status_code=200)

    def test_managers_can_create_students(self):
        self.client.login(username='kyllo', password='password')
        response = self.client.post('/api/schools/1/students/create/', 
            {
                'username':'newstudent', 
                'email':'newstudent@newstudent.com',
                'first_name':'New',
                'last_name':'Student',
                'password1':'newstudent',
                'password2':'newstudent',
            }, 
            follow=True)
        self.assertContains(response,"New Student", status_code=200)

    def test_students_cannot_create_students(self):
        self.client.login(username='ruby', password='ruby')
        response = self.client.post('/api/schools/1/students/create/', 
            {
                'username':'newstudent2', 
                'email':'newstudent@newstudent.com',
                'first_name':'New',
                'last_name':'Student2',
                'password1':'newstudent2',
                'password2':'newstudent2',
            }, 
            follow=True)
        self.assertEqual(response.status_code, 403)

class TestInstructorViews(TestCase):
    fixtures = ['users.json', 'groups.json', 'schools.json',]
    def setUp(self):
        self.client = Client()

    def test_managers_can_create_instructors(self):
        self.client.login(username='kyllo', password='password')
        response = self.client.post('/api/schools/1/instructors/create/', 
            {
                'username':'newinstructor', 
                'email':'new@instructor.com',
                'first_name':'New',
                'last_name':'Instructor',
                'password1':'newinstructor',
                'password2':'newinstructor',
            }, 
            follow=True)
        self.assertContains(response,"New Instructor", status_code=200)

    def test_managers_can_view_school_instructors_list(self):
        self.client.login(username='kyllo', password='password')
        response = self.client.get('/api/schools/1/instructors/')
        self.assertContains(response, 'Alex Kyllo', status_code=200)

    def test_managers_can_view_school_instructors_detail(self):
        self.client.login(username='kyllo', password='password')
        response = self.client.get('/api/users/kyllo/')
        self.assertContains(response, 'Alex Kyllo', status_code=200)

    def test_students_cannot_create_instructors(self):
        self.client.login(username='ruby', password='ruby')
        response = self.client.post('/api/schools/1/instructors/create/', 
            {
                'username':'newinstructor2', 
                'email':'new@instructor.com',
                'first_name':'New',
                'last_name':'Student2',
                'password1':'newinstructor2',
                'password2':'newinstructor2',
            }, 
            follow=True)
        self.assertEqual(response.status_code, 403)       

class TestSchoolViewsWithFixtures(TestCase):
    fixtures = ['schools.json', 'users.json', 'groups.json']

    def setUp(self):
        self.client = Client()

    def test_user_can_view_own_schools_list(self):
        self.client.login(username='kyllo', password='password')
        response = self.client.get('/api/schools/')
        self.assertContains(response, "A Cool School", status_code=200)

    def test_user_cannot_view_other_schools_list(self):
        self.client.login(username='kyllo', password='password')
        response = self.client.get('/api/schools/')
        self.assertNotContains(response, "A Cooler School")

    def test_user_can_view_own_school_detail(self):
        self.client.login(username='kyllo', password='password')
        response = self.client.get('/api/schools/1/')
        self.assertContains(response, "A Cool School", status_code=200)        

    def test_user_cannot_view_other_schools_detail(self):
        self.client.login(username='kyllo', password='password')
        response = self.client.get('/api/schools/2/')
        self.assertEqual(response.status_code, 404)

    def test_anon_user_cannot_view_schools_list(self):
        anon_client = Client()
        response = anon_client.get('/api/schools/')
        self.assertEqual(response.status_code, 403)

    def test_manager_can_delete_own_school(self):
        self.client.login(username='kyllo', password='password')
        response = self.client.post('/api/schools/1/delete/', follow=True)
        self.assertRedirects(response, '/api/schools/', target_status_code=200)
        self.assertNotContains(response, "A Cool School", status_code=200)

    def test_student_cannot_delete_school(self):
        self.client.login(username='ruby', password='ruby')
        response = self.client.post('/api/schools/1/delete/')
        self.assertEqual(response.status_code, 403)

    def test_manager_cannot_delete_other_school(self):
        self.client.login(username='kyllo', password='password')
        response = self.client.post('/api/schools/2/delete/')
        self.assertEqual(response.status_code, 404)

class TestLocationViews(TestCase):
    fixtures = ['schools.json', 'users.json', 'groups.json', 'locations.json']

    def setUp(self):
        self.client = Client()

    def test_user_can_view_location_list_of_own_school(self):
        self.client.login(username='kyllo', password='password')
        response = self.client.get('/api/schools/1/locations/')
        self.assertContains(response, "A Cool School Kirkland Location", status_code=200)

    def test_user_cannot_view_location_list_of_other_school(self):
        self.client.login(username='kyllo', password='password')
        response = self.client.get('/api/schools/2/locations/')
        self.assertEqual(response.status_code, 404)

    def test_user_can_view_location_detail_of_own_school(self):
        self.client.login(username='kyllo',password='password')
        response = self.client.get('/api/locations/1/')
        self.assertContains(response, "A Cool School Kirkland Location", status_code=200)

    def test_user_cannot_view_location_detail_of_other_school(self):
        self.client.login(username='kyllo',password='password')
        response = self.client.get('/api/locations/2/')
        self.assertEqual(response.status_code, 404)

    def test_user_cannot_create_location_for_other_school(self):
        self.client.login(username='kyllo',password='password')
        response = self.client.post('/api/schools/2/locations/create/', 
            {
                'school_id': 2, 
                'name':'a school', 
                'address_1': 'a', 
                'address_2': 'a', 
                'city': 'a', 
                'state_province': 'WA',
                'zip_postal_code': '12345',
                'country': 'US',
            })
        self.assertEqual(response.status_code, 404)

    def test_anonymous_user_cannot_view_location_list(self):
        anon_client = Client()
        response = anon_client.get('/api/schools/1/locations/')
        self.assertEqual(response.status_code, 403)

    def test_anonymous_user_cannot_view_location_detail(self):
        anon_client = Client()
        response = anon_client.get('/api/locations/1/')
        self.assertEqual(response.status_code, 403)

class TestCourseViews(TestCase):
    fixtures = ['schools.json', 'locations.json', 'courses.json', 'users.json', 'groups.json']

    def setUp(self):
        self.client = Client()

    def test_user_can_view_course_list_of_own_school(self):
        self.client.login(username='kyllo',password='password')
        response = self.client.get('/api/locations/1/courses/')
        self.assertContains(response, "Yoga 101", status_code=200)  

    def test_user_cannot_view_course_list_of_other_school(self):
        self.client.login(username='kyllo',password='password')
        response = self.client.get('/api/locations/2/courses/')
        self.assertEqual(response.status_code, 404)

    def test_user_can_view_course_detail_of_own_school(self):
        self.client.login(username='kyllo',password='password')
        response = self.client.get('/api/courses/1/')
        self.assertContains(response, "Yoga 101", status_code=200)  

    def test_user_cannot_view_course_detail_of_other_school(self):
        self.client.login(username='kyllo',password='password')
        response = self.client.get('/api/courses/2/')
        self.assertEqual(response.status_code, 404)

    def test_anonymous_user_cannot_view_course_list(self):
        anon_client = Client()
        response = anon_client.get('/api/locations/1/courses/')
        self.assertEqual(response.status_code, 403)
