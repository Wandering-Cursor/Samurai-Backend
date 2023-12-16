from django.contrib import admin

from accounts.models import Student

from .base_user import BaseUserAdmin


@admin.register(Student)
class StudentAdmin(BaseUserAdmin):
	class Meta:
		model = Student
