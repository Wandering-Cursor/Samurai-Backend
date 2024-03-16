from fastapi import HTTPException


class SamuraiAPIError(HTTPException):
    status_code: int = 400
    error_name: str = "BaseError"
    detail: str | dict = "Base Error"

    def __init__(self: "SamuraiAPIError") -> None:
        super().__init__(
            status_code=self.status_code,
            detail=self.detail,
            headers={
                "X-Error": self.error_name,
            },
        )


class SamuraiIntegrityError(SamuraiAPIError):
    error_name: str = "IntegrityError"
    status_code: int = 409
    detail: str = "Database Integrity Error"
