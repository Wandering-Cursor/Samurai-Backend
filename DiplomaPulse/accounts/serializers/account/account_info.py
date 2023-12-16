from rest_framework import serializers

from ...models import BaseUser, Faculty, Group, Overseer, Student, Teacher


class BaseUserInfoSerializer(serializers.ModelSerializer):
	class Meta:
		model = BaseUser
		fields = [
			"id",
			"email",
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
	group = GroupInfoSerializer(read_only=True)

	class Meta(BaseUserInfoSerializer.Meta):
		model = Student
		fields = BaseUserInfoSerializer.Meta.fields + [
			"group",
		]
		read_only_fields = fields


class TeacherInfoSerializer(BaseUserInfoSerializer):
	class Meta(BaseUserInfoSerializer.Meta):
		model = Teacher
		fields = BaseUserInfoSerializer.Meta.fields + [
			"faculties",
			"contact_information",
		]
		read_only_fields = fields


class OverseerInfoSerializer(BaseUserInfoSerializer):
	class Meta(BaseUserInfoSerializer.Meta):
		model = Overseer
		fields = BaseUserInfoSerializer.Meta.fields + [
			"faculty",
		]
		read_only_fields = fields


class AllUsersInfoSerializer(serializers.Serializer):
	base = BaseUserInfoSerializer()
	student = StudentInfoSerializer()
	teacher = TeacherInfoSerializer()
	overseer = OverseerInfoSerializer()


class AccountInfoSerializer(serializers.Serializer):
	def to_representation(self, instance: BaseUser):
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
