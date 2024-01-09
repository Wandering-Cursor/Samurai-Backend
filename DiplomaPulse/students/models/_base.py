from uuid import uuid4

from django.db import models


class BaseModel(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	@property
	def get_id(self):
		return self.id

	class Meta:
		abstract = True
