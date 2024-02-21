from enum import Enum


class AccountTypeEnum(Enum):
    BASE = "Base user"
    STUDENT = "Student"
    TEACHER = "Teacher"
    OVERSEER = "Overseer"

    @classmethod
    def choices(cls) -> tuple[tuple[str, str], ...]:
        return tuple((i.value, i.value) for i in cls)
