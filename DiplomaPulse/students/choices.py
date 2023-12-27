from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _


class TaskState(TextChoices):
	NEW = "new", _("New")
	IN_PROGRESS = "in_progress", _("In progress")
	IN_REVIEW = "in_review", _("In review")
	REOPENED = "reopened", _("Reopened")
	DONE = "done", _("Done")
