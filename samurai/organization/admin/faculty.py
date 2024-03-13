from django.contrib import admin

from samurai.organization.models.faculty import Faculty


@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    class Meta:
        model = Faculty
