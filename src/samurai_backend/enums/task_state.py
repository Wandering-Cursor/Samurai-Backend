from enum import StrEnum


class TaskState(StrEnum):
    OPEN = "open"
    RESUBMIT = "resubmit"
    IN_PROGRESS = "in_progress"
    IN_REVIEW = "in_review"
    DONE = "done"
