from dal import autocomplete
from django import forms
from django.contrib import admin

from students.models import UserProject


class UserProjectForm(forms.ModelForm):
    class Meta:
        model = UserProject
        fields = "__all__"
        widgets = {
            "student": autocomplete.ModelSelect2(url="student_autocomplete"),
            "supervisor": autocomplete.ModelSelect2(url="teacher_autocomplete"),
        }


@admin.register(UserProject)
class AdminUserProject(admin.ModelAdmin):
    form = UserProjectForm
