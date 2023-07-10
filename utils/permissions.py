# permissions.py

from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied

from apps.sm_accounts.models import ValidateEmail


class CustomPermission(BasePermission):

    def has_permission(self, request, view):

        if request.user.is_authenticated and ValidateEmail.objects.get(user_id=request.user.id).is_active:
            return True
        
        if request.user.is_authenticated and ValidateEmail.objects.get(user_id=request.user.id).is_verified == False :
            raise PermissionDenied("Permission denide, User email is not verified.", code='custom_permission')

