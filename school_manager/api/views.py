# CBVs for API Viewsets
from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import BasicAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView
from api.permissions import IsManager, IsMember, IsManagerOrInstructor
from api.serializers import (
    UserSerializer, GroupSerializer, SchoolSerializer, LocationSerializer, CourseSerializer,
)
from django.contrib.auth.models import User, Group
from django.contrib.auth import login, logout
from schools.models import School, Location, Course, Session

class AuthView(APIView):
    #authentication_classes = (BasicAuthentication,)

    def post(self, request, *args, **kwargs):
        login(request, request.user)
        return Response(UserSerializer(request.user).data)

    def delete(self, request, *args, **kwargs):
        logout(request)
        return Response()

class SchoolStudentListView(generics.ListAPIView):
    authentication_classes = (BasicAuthentication,)
    serializer_class = UserSerializer

    def get_queryset(self, *args, **kwargs):
        return User.objects.filter(groups__name='Students', school__id=self.kwargs.get('school_id'), school__members=self.request.user)

class SchoolCourseListView(generics.ListAPIView):
    authentication_classes = (BasicAuthentication,)
    serializer_class = CourseSerializer

    def get_queryset(self, *args, **kwargs):
        return Course.objects.filter(school__id=self.kwargs.get('school_id'), school__members=self.request.user)

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    model = User
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, IsManager,)

    def get_queryset(self):
        return User.objects.filter(groups__name='Students', school__members=self.request.user)
    
class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (IsAuthenticated, IsManager,)

class SchoolViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows schools to be viewed or edited.
    """
    model = School
    serializer_class = SchoolSerializer
    permission_classes = (IsAuthenticated, IsManager, IsMember,)
    def post_save(self, obj, created=False):
        obj.members = [self.request.user,]

    def get_queryset(self):
        return School.objects.filter(members=self.request.user)

class LocationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows locations to be viewed or edited.
    """
    model = Location
    permission_classes = (IsAuthenticated, IsMember,)
    serializer_class = LocationSerializer
    def get_queryset(self):
        return Location.objects.filter(school__members=self.request.user)

class CourseViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Courses to be viewed or edited.
    """
    model = Course
    permission_classes = (IsAuthenticated, IsMember,)
    serializer_class = CourseSerializer
    def get_queryset(self):
        return Course.objects.filter(location__school__members=self.request.user)

class StudentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Users in the Students group to be viewed or edited.
    """
    model = User
    permission_classes = (IsAuthenticated, IsManagerOrInstructor, IsMember,)
    serializer_class = UserSerializer
    def get_queryset(self):
        return User.objects.filter(groups__name='Students', school__members=self.request.user)

class InstructorViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Users in the Students group to be viewed or edited.
    """
    model = User
    permission_classes = (IsAuthenticated, IsMember,)
    serializer_class = UserSerializer
    def get_queryset(self):
        return User.objects.filter(groups__name='Instructors', school__members=self.request.user)