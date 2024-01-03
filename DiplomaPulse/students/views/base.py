from rest_framework.permissions import IsAuthenticated

from accounts.models import BaseUser, Student
from DiplomaPulse.views import AuthenticatedApiView


class IsStudent(IsAuthenticated):
	def has_permission(self, request, view):
		base_value = super().has_permission(request, view)
		if not base_value:
			return False

		user: BaseUser = request.user
		return isinstance(user.concrete, Student)


class StudentView(AuthenticatedApiView):
	permission_classes = [IsStudent]
