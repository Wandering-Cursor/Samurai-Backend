from django.contrib import admin

from administration.models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
	class Meta:
		model = Task
