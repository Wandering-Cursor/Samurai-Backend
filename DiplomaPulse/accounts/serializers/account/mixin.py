from rest_framework import serializers

from accounts.models import BaseUser, Student, Teacher


class AccountSerializerMixIn(serializers.Serializer):
    user: BaseUser = None

    def validate(self, attrs: dict) -> dict:
        value = super().validate(attrs)

        request = self.context.get("request")
        if not request:
            raise serializers.ValidationError("Request not supplied")

        user = BaseUser.objects.filter(id=request.user.id).first()
        if not user:
            raise serializers.ValidationError("User not found")
        self.user = user

        return value


class StudentSerializerMixIn(AccountSerializerMixIn):
    student_entity: Student = None

    def validate(self, attrs: dict) -> dict:
        value = super().validate(attrs)

        if not isinstance(self.user.concrete, Student):
            raise serializers.ValidationError("Authenticated user is not a student")

        self.student_entity = self.user.concrete
        return value


class TeacherSerializerMixIn(AccountSerializerMixIn):
    teacher_entity: Teacher = None

    def validate(self, attrs: dict) -> dict:
        value = super().validate(attrs)

        if not isinstance(self.user.concrete, Teacher):
            raise serializers.ValidationError("Authenticated user is not a teacher")

        self.teacher_entity = self.user.concrete
        return value
