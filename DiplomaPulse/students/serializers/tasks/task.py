from accounts.serializers.account.account_info import ShortTeacherInfoSerializer
from core.serializers.models import ModelWithUUID
from students.models import UserTask


class TaskSerializer(ModelWithUUID):
	reviewer = ShortTeacherInfoSerializer(allow_null=True)

	class Meta:
		model = UserTask
		fields = [
			"id",
			"order",
			"name",
			"description",
			"state",
			"reviewer",
			"due_date",
			"comments",  # Probably won't work, something has to be done for this
			"updated_at",
		]
