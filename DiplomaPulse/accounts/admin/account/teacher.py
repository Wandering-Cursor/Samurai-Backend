from accounts.models import Teacher
from django.contrib import admin

from .base_user import BaseUserAdmin


@admin.register(Teacher)
class TeacherAdmin(BaseUserAdmin):
	class Meta:
		model = Teacher
