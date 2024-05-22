import pydantic

from samurai_backend.organization.schemas.faculty import FacultyRepresentation


class FacultyRepresentationMixin(pydantic.BaseModel):
    faculty_id: pydantic.UUID4 | None = None

    @pydantic.computed_field
    @property
    def faculty_details(self: "FacultyRepresentationMixin") -> FacultyRepresentation | None:
        from samurai_backend.organization.get.faculty import get_faculty_by_id

        if not self.faculty_id:
            return None
        return FacultyRepresentation.model_validate(
            get_faculty_by_id(self.faculty_id),
            from_attributes=True,
        )
