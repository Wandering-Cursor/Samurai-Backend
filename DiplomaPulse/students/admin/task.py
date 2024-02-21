from dal import autocomplete
from django import forms
from django.contrib import admin

from students.models import UserTask


class UserTaskForm(forms.ModelForm):
    class Meta:
        model = UserTask
        fields = "__all__"
        widgets = {
            "reviewer": autocomplete.ModelSelect2(url="teacher_autocomplete"),
        }


@admin.register(UserTask)
class AdminUserTask(admin.ModelAdmin):
    form = UserTaskForm
    readonly_fields = ["comments"]
