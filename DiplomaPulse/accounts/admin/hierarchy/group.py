from django.contrib import admin

from accounts.models import Group


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
	class Meta:
		model = Group
