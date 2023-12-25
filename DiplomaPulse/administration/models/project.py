from django.db import models

from ._base import BaseModel


class Project(BaseModel):
	name = models.CharField(max_length=255)
	description = models.TextField()
	for_faculty = models.ForeignKey(
		"accounts.Faculty",
		on_delete=models.CASCADE,
		related_name="projects",
	)
	tasks = models.ManyToManyField(
		"Task",
		related_name="projects",
	)

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = "Project"
		verbose_name_plural = "Projects"
