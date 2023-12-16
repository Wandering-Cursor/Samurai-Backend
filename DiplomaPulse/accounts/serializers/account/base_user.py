from accounts.models.base_user import BaseUser
from rest_framework import serializers


class BaseUserShortInfoSerializer(serializers.ModelSerializer):
	class Meta:
		model = BaseUser
		fields = [
			"id",
			"email",
		]
