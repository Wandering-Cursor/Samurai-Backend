from django.db.models import Q

from accounts.models import Overseer

from .base_user import BaseUserAutocomplete


class OverseerAutocomplete(BaseUserAutocomplete):
	model = Overseer

	def get_q_filters(self):
		super_filters = super().get_q_filters()
		super_filters |= Q(faculty__name=self.q)
		return super_filters
