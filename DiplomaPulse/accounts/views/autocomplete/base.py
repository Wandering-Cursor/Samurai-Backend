from dal import autocomplete
from django.core.exceptions import PermissionDenied


class BaseAutocomplete(autocomplete.Select2QuerySetView):
	model = None

	def get_queryset(self):
		if not self.model:
			raise ValueError("Model is not defined")

		if not self.request.user.is_authenticated:
			raise PermissionDenied()
		if not self.request.user.is_staff:
			raise PermissionDenied()

		return self.model.objects.all()
