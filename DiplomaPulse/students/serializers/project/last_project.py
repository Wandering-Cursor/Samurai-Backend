from typing import TypedDict
from uuid import UUID

from accounts.models import Student
from accounts.serializers.account.account_info import ShortTeacherInfoSerializer
from accounts.serializers.account.mixin import StudentSerializerMixIn
from core.serializers.models import ModelWithUUID
from students.models import UserProject


class ValidatedData(TypedDict):
	account_uuid: UUID
	student: Student


class UserProjectSerializer(ModelWithUUID):
	supervisor = ShortTeacherInfoSerializer()

	class Meta:
		model = UserProject
		fields = "__all__"


class LastProjectSerializer(StudentSerializerMixIn):
	def validate(self, attrs):
		attrs = super().validate(attrs)

		attrs["student"] = self.student_entity

		return attrs

	def create(self, validated_data: ValidatedData):
		return UserProject.objects.filter(student=validated_data["student"]).last()
