from django.contrib import admin

from accounts.models import Teacher

from .base_user import BaseUserAdmin


@admin.register(Teacher)
class TeacherAdmin(BaseUserAdmin):
    class Meta:
        model = Teacher
