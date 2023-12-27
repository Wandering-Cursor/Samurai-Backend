from django.db.models import Q

from accounts.models import Teacher

from .base_user import BaseUserAutocomplete


class TeacherAutocomplete(BaseUserAutocomplete):
	model = Teacher

	def get_q_filters(self):
		super_filters = super().get_q_filters()
		super_filters |= Q(faculties__name=self.q)
		return super_filters
