import pydantic


class RegisterAccount(pydantic.BaseModel):
    email: pydantic.EmailStr = pydantic.Field(
        description="The email of the account.",
    )
    username: str | None = pydantic.Field(
        default=None,
        description="Set a username for the account. (Optional)",
    )
    registration_code: str = pydantic.Field(
        description="The registration code for the account.",
    )

    password: str = pydantic.Field(
        description="The password of the account.",
        min_length=8,
    )


class RegisterAccountResponse(pydantic.BaseModel):
    status: str = pydantic.Field(default="success")


class ConfirmEmail(pydantic.BaseModel):
    email_code: str = pydantic.Field(
        description="The code from email to confirm the registration.",
    )


class ConfirmEmailResponse(RegisterAccountResponse):
    pass
