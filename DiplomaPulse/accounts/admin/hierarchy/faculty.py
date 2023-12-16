from django.contrib import admin

from accounts.models import Faculty


@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
	class Meta:
		model = Faculty
