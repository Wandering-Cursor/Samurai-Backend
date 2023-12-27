from django.db.models import Q

from accounts.models import Student

from .base_user import BaseUserAutocomplete


class StudentAutocomplete(BaseUserAutocomplete):
	model = Student

	def get_q_filters(self):
		super_filters = super().get_q_filters()
		super_filters |= Q(group__name=self.q)
		return super_filters
