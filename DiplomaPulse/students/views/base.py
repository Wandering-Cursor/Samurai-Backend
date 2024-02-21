from typing import TYPE_CHECKING

from accounts.models import BaseUser, Student
from rest_framework.permissions import IsAuthenticated

from DiplomaPulse.views import AuthenticatedApiView

if TYPE_CHECKING:
    from rest_framework.request import Request
    from rest_framework.views import APIView


class IsStudent(IsAuthenticated):
    def has_permission(self, request: "Request", view: "APIView") -> bool:
        base_value = super().has_permission(request, view)
        if not base_value:
            return False

        user: BaseUser = request.user
        return isinstance(user.concrete, Student)


class StudentView(AuthenticatedApiView):
    permission_classes = [IsStudent]
