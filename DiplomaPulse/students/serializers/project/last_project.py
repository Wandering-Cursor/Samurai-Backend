from typing import TypedDict
from uuid import UUID

from rest_framework import serializers

from accounts.models import Student
from accounts.serializers.account.account_info import ShortTeacherInfoSerializer
from students.models import UserProject


class ValidatedData(TypedDict):
	account_uuid: UUID
	student: Student


class UserProjectSerializer(serializers.ModelSerializer):
	supervisor = ShortTeacherInfoSerializer()

	class Meta:
		model = UserProject
		fields = [
			"theme",
			"description",
			"supervisor",
		]
		read_only_fields = fields


class LastProjectSerializer(serializers.Serializer):
	account_uuid = serializers.UUIDField(required=True)
	student_entity: Student = None

	def validate_account_uuid(self, value):
		student = Student.objects.filter(id=value).first()
		if not student:
			raise serializers.ValidationError("Student not found")

		self.student_entity = student

		return value

	def validate(self, attrs):
		attrs = super().validate(attrs)

		self.validate_account_uuid(attrs["account_uuid"])

		attrs["student"] = self.student_entity

		return attrs

	def create(self, validated_data: ValidatedData):
		return UserProject.objects.filter(student=validated_data["student"]).last()
