from accounts.serializers.account.mixin import StudentSerializerMixIn
from rest_framework import serializers

from students.serializers.tasks.task import TaskFinderMixin, TaskSerializer


class TaskDetailsInputSerializer(serializers.Serializer):
    task_id = serializers.UUIDField()


class TaskDetailsOutputSerializer(TaskSerializer):
    pass


class GetTaskDetailsSerializer(StudentSerializerMixIn, TaskDetailsInputSerializer, TaskFinderMixin):
    def create(self) -> TaskDetailsOutputSerializer:
        return TaskDetailsOutputSerializer(self.task)
