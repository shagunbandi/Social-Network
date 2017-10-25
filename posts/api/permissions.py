from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerOrReadOnly(BasePermission):
    message = 'Must be the owner of the object'
    my_safe_methods = ['GET']

    # def has_permission(self, request, view):
    #     if request.method in self.my_safe_methods:
    #         return True
    #     return False

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.user == request.user
