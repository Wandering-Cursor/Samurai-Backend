import pydantic

from samurai_backend.organization.schemas.department import DepartmentRepresentation


class DepartmentRepresentationMixin(pydantic.BaseModel):
    department_id: pydantic.UUID4 | None = None

    @pydantic.computed_field
    @property
    def department_details(
        self: "DepartmentRepresentationMixin",
    ) -> DepartmentRepresentation | None:
        from samurai_backend.db import get_db_session
        from samurai_backend.organization.get.department import get_department_by_id

        generator = get_db_session()
        session = next(generator)

        if not self.department_id:
            return None
        return DepartmentRepresentation.model_validate(
            get_department_by_id(session, self.department_id),
            from_attributes=True,
        )
