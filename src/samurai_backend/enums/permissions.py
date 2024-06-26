from enum import StrEnum

from fastapi import Security


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

    PROJECTS_STATS = "projects_stats"

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
    def as_security(self: "Permissions") -> Security:
        from samurai_backend.dependencies.get_current_active_account import (
            get_current_active_account,
        )

        return Security(
            get_current_active_account,
            scopes=[self],
        )

    @classmethod
    def blank_security(cls: "Permissions") -> Security:
        from samurai_backend.dependencies.get_current_active_account import (
            get_current_active_account,
        )

        return Security(
            get_current_active_account,
            scopes=[],
        )
