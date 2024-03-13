from django.contrib import admin

from samurai.organization.models.group import Group


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    class Meta:
        model = Group
