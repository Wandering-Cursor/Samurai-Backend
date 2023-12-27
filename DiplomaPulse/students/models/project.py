from django.db import models

from ._base import BaseModel


class UserProject(BaseModel):
	theme = models.CharField(max_length=255)
	description = models.TextField()

	student = models.ForeignKey(
		"accounts.Student",
		related_name="user_projects",
		on_delete=models.CASCADE,
	)
	supervisor = models.ForeignKey(
		"accounts.Teacher",
		related_name="user_projects",
		on_delete=models.CASCADE,
	)

	tasks = models.ManyToManyField(
		"UserTask",
		related_name="user_projects",
	)

	class Meta:
		ordering = ["-created_at"]

	def __str__(self):
		return f"UserProject: {self.theme} by {self.student}"
