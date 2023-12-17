import logging
from typing import TypedDict

from django.db import transaction
from rest_framework import serializers

from accounts.models.base_user import BaseUser

from ..errors.account.sign_up import RegistrationCodeNotFound
from .base_user import BaseUserShortInfoSerializer


class ValidatedData(TypedDict):
	email: str
	password: str
	registration_code: str
	user: BaseUser


class SignUpSerializer(serializers.Serializer):
	email = serializers.EmailField(
		required=True, max_length=BaseUser._meta.get_field("email").max_length
	)
	password = serializers.CharField(required=True, min_length=8)
	registration_code = serializers.CharField(required=True)

	def validate(self, attrs) -> ValidatedData:
		attrs = super().validate(attrs)

		user_entity = BaseUser.objects.get_user_by_registration_code(
			attrs["registration_code"],
		)

		if not user_entity:
			raise RegistrationCodeNotFound

		attrs["user"] = user_entity

		return ValidatedData(**attrs)

	@transaction.atomic
	def create(
		self,
		validated_data: ValidatedData,
		return_representation: bool = False,
	) -> BaseUser | BaseUserShortInfoSerializer:
		user_entity = validated_data["user"]

		user_with_email = BaseUser.objects.filter(email=validated_data["email"]).first()
		if user_with_email:
			# Safety precaution
			# We do not want to let anyone know that this email is already in use
			# So we just return the same response as if the user was created
			logging.warn("User with this email already exists")
			user_entity = user_with_email
		else:
			# We generate default email, but we need to set it to an actual one
			user_entity.email = validated_data["email"]
			user_entity.set_password(validated_data["password"])
			# Removing registration code, so it cannot be used again
			user_entity.registration_code = None

			user_entity.save()
			logging.info(f"User was created successfully - {user_entity}")

		result = user_entity
		if return_representation:
			result = BaseUserShortInfoSerializer(instance=user_entity)

		return result
