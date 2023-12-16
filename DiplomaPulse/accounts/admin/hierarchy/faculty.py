from accounts.models import Faculty
from django.contrib import admin


@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
	class Meta:
		model = Faculty
