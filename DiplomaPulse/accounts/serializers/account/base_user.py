from rest_framework import serializers
from accounts.models.base_user import BaseUser


class BaseUserShortInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseUser
        fields = [
            "id",
            "email",
        ]
