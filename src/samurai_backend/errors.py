from fastapi import HTTPException, status


class SamuraiAPIError(HTTPException):
    status_code: int = status.HTTP_400_BAD_REQUEST
    error_name: str = "BaseError"
    detail: str | dict = "Base Error"

    def __init__(
        self: "SamuraiAPIError",
        detail_override: str | None = None,
    ) -> None:
        if detail_override is not None:
            self.detail = detail_override

        super().__init__(
            status_code=self.status_code,
            detail=self.detail,
            headers={
                "X-Error": self.error_name,
            },
        )


class SamuraiIntegrityError(SamuraiAPIError):
    error_name: str = "IntegrityError"
    status_code: int = status.HTTP_409_CONFLICT
    detail: str = "Database Integrity Error"


class SamuraiNotFoundError(SamuraiAPIError):
    error_name: str = "NotFoundError"
    status_code: int = status.HTTP_404_NOT_FOUND
    detail: str = "Resource Not Found"


class SamuraiInvalidRequestError(SamuraiAPIError):
    error_name: str = "InvalidRequestError"
    status_code: int = status.HTTP_400_BAD_REQUEST
    detail: str = "Invalid Request"


class SamuraiForbiddenError(SamuraiAPIError):
    error_name: str = "ForbiddenError"
    status_code: int = status.HTTP_403_FORBIDDEN
    detail: str = "Forbidden"


class SamuraiValidationError(SamuraiAPIError):
    error_name: str = "ValidationError"
    status_code: int = status.HTTP_422_UNPROCESSABLE_ENTITY
    detail: dict = {"msg": "Validation Error"}

    def __init__(
        self: "SamuraiValidationError",
        detail: dict | None = None,
        message: str | None = None,
    ) -> None:
        detail_override = {
            "msg": "Validation Error",
            "type": self.error_name,
        }

        if detail is not None:
            detail_override = detail
            if "msg" not in detail_override:
                detail_override["msg"] = "Validation Error"
        if message is not None:
            detail_override["msg"] = message

        super().__init__(detail_override=detail_override)
