from accounts.serializers.account.account_info import ShortTeacherInfoSerializer
from core.serializers.models import ModelWithUUID
from rest_framework import serializers, status

from students.models import UserTask


class TaskSerializer(ModelWithUUID):
    reviewer = ShortTeacherInfoSerializer(allow_null=True)

    class Meta:
        model = UserTask
        fields = "__all__"


class TaskNotFound(serializers.Serializer):
    error = serializers.CharField(default="TASK_NOT_FOUND")
    details = serializers.CharField(default="Task with specified task_id is not found")
    code = serializers.IntegerField(default=status.HTTP_404_NOT_FOUND)


class TaskFinderMixin:
    """All serializers using this Mixin must have a property `student_entity`"""

    task: UserTask = None

    def validate_task_id(self, task_id: str) -> str:
        task_not_found = Exception(
            TaskNotFound(
                data={
                    "details": f"Task not found with {task_id=}",
                }
            )
        )

        qs = UserTask.objects.filter(id=task_id)
        task = qs.first()
        if not task:
            raise task_not_found

        if not task.user_projects.filter(student=self.student_entity).exists():
            raise task_not_found

        self.task = task

        return task.id
