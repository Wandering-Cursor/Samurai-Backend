from rest_framework import serializers

from accounts.serializers.account.mixin import StudentSerializerMixIn
from students.serializers.tasks.task import TaskFinderMixin, TaskSerializer


class TaskDetailsInputSerializer(serializers.Serializer):
	task_id = serializers.UUIDField()


class TaskDetailsOutputSerializer(TaskSerializer):
	pass


class GetTaskDetailsSerializer(StudentSerializerMixIn, TaskDetailsInputSerializer, TaskFinderMixin):
	def create(self):
		return TaskDetailsOutputSerializer(self.task)
