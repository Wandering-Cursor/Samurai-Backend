from django.contrib import admin

from administration.models import Project


class TasksInline(admin.TabularInline):
    model = Project.tasks.through
    ordering = ["task__order"]
    extra = 1


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "name",
        "for_faculty",
        "created_at",
        "updated_at",
    ]
    inlines = [
        TasksInline,
    ]

    exclude = ["tasks"]

    class Meta:
        model = Project
