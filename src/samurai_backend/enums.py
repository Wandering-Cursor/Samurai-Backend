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

    COMMENTS = "comments"
    COMMENTS_READ = "comments:read"
    COMMENTS_UPDATE = "comments:update"
    COMMENTS_DELETE = "comments:delete"
    COMMENTS_CREATE = "comments:create"
