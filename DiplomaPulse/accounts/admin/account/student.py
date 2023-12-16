from accounts.models import Student
from django.contrib import admin

from .base_user import BaseUserAdmin


@admin.register(Student)
class StudentAdmin(BaseUserAdmin):
	class Meta:
		model = Student
