from enum import Enum, StrEnum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from fastapi import Security


class AccountType(Enum):
    ADMIN = "admin"
    STUDENT = "student"
    TEACHER = "teacher"
    OVERSEER = "overseer"


class Permissions(StrEnum):
    ADMIN = "admin"

    ACCOUNTS_SEARCH = "accounts:search"

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

    CHATS = "chat"
    CHATS_READ = "chat:read"
    CHATS_UPDATE = "chat:update"
    CHATS_ADD_MEMBER = "chat:add_member"
    CHATS_CREATE = "chat:create"

    MESSAGES = "messages"
    MESSAGES_READ = "messages:read"
    MESSAGES_UPDATE = "messages:update"
    MESSAGES_DELETE = "messages:delete"
    MESSAGES_CREATE = "messages:create"

    @property
    def description(self: "Permissions") -> str:
        message = ""

        default = self.value.replace("_", " ").title()
        if ":" in default:
            split = default.split(":")
            permission_name = split[0].replace("_", " ").title()
            action = split[1].replace("_", " ").title()

            message = f"A {permission_name} user that can do: {action}"
        else:
            message = f"A user that can operate {default}."

        return message

    @property
    def as_security(self: "Permissions") -> "Security":
        from fastapi import Security

        from samurai_backend.dependencies import get_current_active_account

        return Security(
            get_current_active_account,
            scopes=[self],
        )

    @classmethod
    def blank_security(cls) -> "Security":
        from fastapi import Security

        from samurai_backend.dependencies import get_current_active_account

        return Security(
            get_current_active_account,
            scopes=[],
        )


class TaskState(StrEnum):
    OPEN = "open"
    RESUBMIT = "resubmit"
    IN_PROGRESS = "in_progress"
    IN_REVIEW = "in_review"
    DONE = "done"
