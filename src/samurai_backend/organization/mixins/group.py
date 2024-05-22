import pydantic

from samurai_backend.organization.schemas.group import Group


class GroupRepresentationMixin(pydantic.BaseModel):
    group_id: pydantic.UUID4 | None = None

    @pydantic.computed_field
    @property
    def group_details(self: "GroupRepresentationMixin") -> Group | None:
        from samurai_backend.organization.get.group import get_group_by_id

        if not self.group_id:
            return None
        return Group.model_validate(get_group_by_id(self.group_id), from_attributes=True)
