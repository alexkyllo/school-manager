from rest_framework import permissions

class IsSchoolManager(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to see it.
    Assumes the model instance has a `manager` attribute.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        #if request.method in permissions.SAFE_METHODS:            
        #    return True

        # Instance must have an attribute named `manager`.
        return obj.manager == request.user

class IsSchoolMember(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.school == request.user.school