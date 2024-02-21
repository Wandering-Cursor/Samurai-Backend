from core.serializers.models import ModelWithUUID
from rest_framework import serializers

from accounts.enums import AccountTypeEnum
from accounts.models import BaseUser, Faculty, Group, Overseer, Student, Teacher


class UserUUID(serializers.ModelSerializer):
    id = serializers.UUIDField()

    def validate_id(self, value: str) -> str:
        # Maybe it's actually a UUID value :shrug:
        if not BaseUser.objects.filter(id=value).exists():
            raise serializers.ValidationError(
                detail=f"User with {value=} was not found",
                code=404,
            )

        return value

    class Meta:
        model = BaseUser
        fields = [
            "id",
        ]
        read_only_fields = fields


class BaseUserInfoSerializer(ModelWithUUID):
    account_type = serializers.CharField(default=AccountTypeEnum.BASE.value, read_only=True)

    class Meta:
        model = BaseUser
        fields = [
            "id",
            "account_type",
            "email",
            "first_name",
            "last_name",
            "middle_name",
            "profile_picture",
        ]
        read_only_fields = fields


class ShortBaseUserInfoSerializer(BaseUserInfoSerializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    account_type = serializers.ChoiceField(
        choices=AccountTypeEnum.choices(),
        source="account_type_value",
    )

    class Meta:
        model = BaseUser
        fields = [
            "id",
            "account_type",
            "first_name",
            "last_name",
            "middle_name",
            "profile_picture",
        ]
        read_only_fields = fields


class FacultyInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Faculty
        fields = [
            "id",
            "name",
        ]
        read_only_fields = fields


class GroupInfoSerializer(serializers.ModelSerializer):
    faculty = FacultyInfoSerializer(read_only=True)

    class Meta:
        model = Group
        fields = [
            "id",
            "name",
            "faculty",
        ]
        read_only_fields = fields


class StudentInfoSerializer(BaseUserInfoSerializer):
    account_type = serializers.CharField(default=AccountTypeEnum.STUDENT.value, read_only=True)
    group = GroupInfoSerializer(read_only=True)

    class Meta(BaseUserInfoSerializer.Meta):
        model = Student
        fields = [
            *BaseUserInfoSerializer.Meta.fields,
            "group",
        ]
        read_only_fields = fields


class TeacherInfoSerializer(BaseUserInfoSerializer):
    account_type = serializers.CharField(default=AccountTypeEnum.TEACHER.value, read_only=True)

    class Meta(BaseUserInfoSerializer.Meta):
        model = Teacher
        fields = [
            *BaseUserInfoSerializer.Meta.fields,
            "faculties",
            "contact_information",
        ]
        read_only_fields = fields


class ShortTeacherInfoSerializer(TeacherInfoSerializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()

    class Meta:
        model = Teacher
        fields = [
            "id",
            "first_name",
            "last_name",
            "middle_name",
            "profile_picture",
        ]
        read_only_fields = fields


class OverseerInfoSerializer(BaseUserInfoSerializer):
    account_type = serializers.CharField(default=AccountTypeEnum.OVERSEER.value, read_only=True)

    class Meta(BaseUserInfoSerializer.Meta):
        model = Overseer
        fields = [
            *BaseUserInfoSerializer.Meta.fields,
            "faculty",
        ]
        read_only_fields = fields


class AllUsersInfoSerializer(serializers.Serializer):
    base = BaseUserInfoSerializer()
    student = StudentInfoSerializer()
    teacher = TeacherInfoSerializer()
    overseer = OverseerInfoSerializer()


class AccountInfoSerializer(serializers.Serializer):
    account_id = serializers.UUIDField(required=False)

    def validate(self, attrs: dict) -> dict:
        attrs = super().validate(attrs)

        if account_id := attrs.get("account_id"):
            user_entity = BaseUser.objects.filter(id=account_id).first()
            if not user_entity:
                raise serializers.ValidationError(
                    {
                        "account_id": "User not found",
                    },
                    code=404,
                )
            self.instance = user_entity

        return attrs

    def to_representation(self, instance: BaseUser) -> dict:
        concrete_instance = instance.concrete
        concrete_type = type(concrete_instance)

        if concrete_type == Student:
            serializer = StudentInfoSerializer(instance=concrete_instance)
        elif concrete_type == Teacher:
            serializer = TeacherInfoSerializer(instance=concrete_instance)
        elif concrete_type == Overseer:
            serializer = OverseerInfoSerializer(instance=concrete_instance)
        else:
            serializer = BaseUserInfoSerializer(instance=concrete_instance)

        return serializer.data
