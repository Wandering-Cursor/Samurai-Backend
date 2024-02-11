from rest_framework import serializers

from accounts.models import BaseUser, Student, Teacher


class AccountSerializerMixIn(serializers.Serializer):
	account_uuid = serializers.UUIDField(required=True)
	user: BaseUser = None

	def validate_account_uuid(self, value):
		user = BaseUser.objects.filter(id=value).first()
		if not user:
			raise serializers.ValidationError("User not found")

		self.user = user

		return value


class StudentSerializerMixIn(AccountSerializerMixIn):
	student_entity: Student = None

	def validate_account_uuid(self, value):
		value = super().validate_account_uuid(value)

		if not isinstance(self.user.concrete, Student):
			raise serializers.ValidationError("Student not found")

		return value


class TeacherSerializerMixIn(AccountSerializerMixIn):
	teacher_entity: Teacher = None

	def validate_account_uuid(self, value):
		value = super().validate_account_uuid(value)

		if not isinstance(self.user.concrete, Teacher):
			raise serializers.ValidationError("Teacher not found")

		return value
