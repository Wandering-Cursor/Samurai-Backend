from enum import Enum, StrEnum


class AccountType(Enum):
    ADMIN = "admin"
    STUDENT = "student"
    TEACHER = "teacher"
    OVERSEER = "overseer"


class Permissions(StrEnum):
    ADMIN = "admin"

    PROJECTS = "projects"
    PROJECTS_READ = "projects:read"
    PROJECTS_UPDATE = "projects:update"
    PROJECTS_DELETE = "projects:delete"
    PROJECTS_CREATE = "projects:create"

    TASKS = "tasks"
    TASKS_READ = "tasks:read"
    TASKS_UPDATE = "tasks:update"

    TASKS_EDITOR = "tasks_editor"
    TASKS_EDITOR_UPDATE = "tasks_editor:update"
    TASKS_EDITOR_DELETE = "tasks_editor:delete"
    TASKS_EDITOR_CREATE = "tasks_editor:create"

    COMMENTS = "comments"
    COMMENTS_READ = "comments:read"
    COMMENTS_UPDATE = "comments:update"
    COMMENTS_DELETE = "comments:delete"
    COMMENTS_CREATE = "comments:create"


class TaskState(StrEnum):
    OPEN = "open"
    RESUBMIT = "resubmit"
    IN_PROGRESS = "in_progress"
    IN_REVIEW = "in_review"
    DONE = "done"
