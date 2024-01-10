from rest_framework import serializers

from accounts.models import Student


class AccountSerializerMixIn(serializers.Serializer):
	account_uuid = serializers.UUIDField(required=True)
	student_entity: Student = None

	def validate_account_uuid(self, value):
		student = Student.objects.filter(id=value).first()
		if not student:
			raise serializers.ValidationError("Student not found")

		self.student_entity = student

		return value
