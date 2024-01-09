from typing import TypedDict
from uuid import UUID

from accounts.models import Student
from accounts.serializers.account.account_info import ShortTeacherInfoSerializer
from core.serializers.models import ModelWithUUID
from students.models import UserProject
from students.serializers.base import AccountSerializerMixIn


class ValidatedData(TypedDict):
	account_uuid: UUID
	student: Student


class UserProjectSerializer(ModelWithUUID):
	supervisor = ShortTeacherInfoSerializer()

	class Meta:
		model = UserProject
		fields = [
			"id",
			"theme",
			"description",
			"supervisor",
		]
		read_only_fields = fields


class LastProjectSerializer(AccountSerializerMixIn):
	def validate(self, attrs):
		attrs = super().validate(attrs)

		# self.validate_account_uuid(attrs["account_uuid"])

		attrs["student"] = self.student_entity

		return attrs

	def create(self, validated_data: ValidatedData):
		return UserProject.objects.filter(student=validated_data["student"]).last()
