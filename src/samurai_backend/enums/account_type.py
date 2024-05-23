from enum import Enum


class AccountType(Enum):
    ADMIN = "admin"
    STUDENT = "student"
    TEACHER = "teacher"
    OVERSEER = "overseer"
