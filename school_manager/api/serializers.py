from django.contrib.auth.models import User, Group
from schools.models import School, Location, Course
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups', 'school_set')

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name', 'user_set',)

class SchoolSerializer(serializers.HyperlinkedModelSerializer):
    locations = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='location-detail')

    class Meta:
        model = School
        fields = ('url', 'name', 'locations', 'members',)

class LocationSerializer(serializers.HyperlinkedModelSerializer):
    courses = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='course-detail')

    class Meta:
        model = Location
        fields = ('url', 'school', 'name', 'courses','address_1', 'address_2', 'city', 'state_province', 'zip_postal_code', 'country')

class CourseSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Course
        fields = ('url', 'location', 'name', 'instructors', 'students')