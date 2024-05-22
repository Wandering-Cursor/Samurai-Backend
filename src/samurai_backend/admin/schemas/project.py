import datetime

import pydantic


class BatchCreateProjectTask(pydantic.BaseModel):
    name: str
    description: str
    priority: int = 0
    reviewer: pydantic.UUID4 | None = None
    due_date: datetime.datetime | None = None


class BatchCreateProject(pydantic.BaseModel):
    name: str
    description: str
    faculty_id: pydantic.UUID4

    tasks: list[BatchCreateProjectTask]
