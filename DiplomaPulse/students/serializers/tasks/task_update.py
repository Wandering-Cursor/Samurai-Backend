from accounts.serializers.account.mixin import StudentSerializerMixIn
from rest_framework import serializers

from students.choices import TaskState
from students.models.task import UserTask
from students.serializers.tasks.task import TaskFinderMixin

ALLOWED_OPERATIONS = {
    TaskState.NEW: [TaskState.IN_PROGRESS],
    TaskState.REOPENED: [TaskState.IN_PROGRESS],
    TaskState.IN_PROGRESS: [TaskState.IN_REVIEW, TaskState.DONE],
}


class UpdateTaskInputSerializer(serializers.Serializer):
    task_id = serializers.UUIDField()
    state = serializers.ChoiceField(choices=TaskState.choices)


class UpdateTaskForbiddenSerializer(serializers.Serializer):
    error = serializers.CharField(default="STATE_CHANGE_FORBIDDEN")
    detail = serializers.CharField(
        help_text="Explains why the change cannot be made in more details"
    )
    code = serializers.IntegerField(default=403)


class UpdateTaskSerializer(StudentSerializerMixIn, UpdateTaskInputSerializer, TaskFinderMixin):
    def create(self, validated_data: dict) -> UserTask:
        task = self.task

        current_state = task.state
        desired_state: TaskState = validated_data["state"]

        if current_state == desired_state:
            return task

        if current_state == TaskState.DONE:
            raise Exception(
                UpdateTaskForbiddenSerializer(
                    data={
                        "detail": f"Cannot update state of completed task ({current_state=})",
                    }
                )
            )
        if current_state == TaskState.IN_REVIEW:
            raise Exception(
                UpdateTaskForbiddenSerializer(
                    data={
                        "detail": f"Cannot change state of task in review ({current_state=})",
                    }
                )
            )

        if current_state == TaskState.IN_PROGRESS:
            if desired_state == TaskState.DONE and task.reviewer:
                raise Exception(
                    UpdateTaskForbiddenSerializer(
                        data={
                            "detail": "This task has a reviewer",
                        }
                    )
                )

            if desired_state == TaskState.IN_REVIEW and not task.reviewer:
                raise Exception(
                    UpdateTaskForbiddenSerializer(
                        data={"detail": "This task doesn't have a reviewer"}
                    )
                )

        if desired_state == TaskState.DONE and current_state != TaskState.IN_PROGRESS:
            raise Exception(
                UpdateTaskForbiddenSerializer(
                    data={
                        "detail": "Task is not in progress",
                    }
                )
            )

        allowed_operations = ALLOWED_OPERATIONS[current_state]
        if desired_state in allowed_operations:
            task.state = desired_state
            task.save()

            return UserTask.objects.filter(id=task.id).first()
        raise Exception(
            UpdateTaskForbiddenSerializer(
                data={
                    "detail": "State change is not allowed (General case)",
                }
            )
        )
