from django.db.models import Q

from accounts.models import BaseUser

from .base import BaseAutocomplete


class BaseUserAutocomplete(BaseAutocomplete):
	model = BaseUser

	def get_q_filters(self):
		return (
			Q(email__icontains=self.q)
			| Q(first_name__icontains=self.q)
			| Q(last_name__icontains=self.q)
		)

	def get_queryset(self):
		qs = super().get_queryset()

		if self.q:
			qs = qs.filter(self.get_q_filters())

		return qs.order_by("pk")
