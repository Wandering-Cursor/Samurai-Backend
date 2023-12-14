from django.db import transaction
from typing import TypedDict
from rest_framework import serializers, exceptions
from accounts.models.base_user import BaseUser


class ValidatedData(TypedDict):
    email: str
    password: str
    registration_code: str
    user: BaseUser


class BaseUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseUser
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
        ]


class SignUpSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, max_length=BaseUser._meta.get_field("email").max_length)
    password = serializers.CharField(required=True, min_length=8)
    registration_code = serializers.CharField(required=True)

    def validate(self, attrs) -> ValidatedData:
        attrs = super().validate(attrs)

        user_entity = BaseUser.objects.get_user_by_registration_code(attrs["registration_code"])

        if not user_entity:
            raise exceptions.NotFound({"registration_code": "Invalid registration code"})

        attrs["user"] = user_entity

        return ValidatedData(**attrs)

    @transaction.atomic
    def create(
        self,
        validated_data: ValidatedData,
        return_representation: bool = False,
    ) -> BaseUser | BaseUserSerializer:
        user_entity = validated_data["user"]

        # We generate default email, but we need to set it to an actual one
        user_entity.email = validated_data["email"]
        user_entity.set_password(validated_data["password"])
        # Removing registration code, so it cannot be used again
        user_entity.registration_code = None

        user_entity.save()

        result = user_entity
        if return_representation:
            result = BaseUserSerializer(instance=user_entity)

        return result
