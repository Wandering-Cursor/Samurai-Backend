import pydantic


class FileRepresentation(pydantic.BaseModel):
    file_id: pydantic.UUID4

    file_name: str
    file_type: str
    file_size: int

    @pydantic.computed_field
    def _links(self) -> dict[str, str]:
        return {
            "download": f"/file/{self.file_id}",
        }

    class Config:
        from_attributes = True
