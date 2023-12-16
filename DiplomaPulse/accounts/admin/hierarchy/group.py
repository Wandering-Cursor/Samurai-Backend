from accounts.models import Group
from django.contrib import admin


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
	class Meta:
		model = Group
