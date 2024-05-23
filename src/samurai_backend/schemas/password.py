import pydantic

from samurai_backend.errors import SamuraiInvalidRequestError


class ResetPasswordInputScheme(pydantic.BaseModel):
    email: str | None = None
    username: str | None = None

    @pydantic.model_validator(mode="after")
    def validate_self(self: "ResetPasswordInputScheme") -> "ResetPasswordInputScheme":
        if not self.email and not self.username:
            raise SamuraiInvalidRequestError("You must provide either an email or a username.")
        if self.email and self.username:
            raise SamuraiInvalidRequestError("You can only provide either an email or a username.")

        return self


class ResetPasswordResponseScheme(pydantic.BaseModel):
    status: str = "success"


class ResetPasswordConfirmInputScheme(pydantic.BaseModel):
    code: str
    new_password: str = pydantic.Field(
        min_length=8,
    )


class ChangePasswordInputScheme(pydantic.BaseModel):
    old_password: str
    new_password: str = pydantic.Field(
        min_length=8,
    )


class ChangePasswordResponseScheme(pydantic.BaseModel):
    status: str = "success"
