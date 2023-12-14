from __future__ import annotations
from typing import TYPE_CHECKING

from django.contrib.auth.models import BaseUserManager

if TYPE_CHECKING:
    from ..models.base_user import BaseUser


class UserManager(BaseUserManager):
    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a superuser with the given email and password.
        """
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user

    def get_user_by_registration_code(self, registration_code) -> "BaseUser | None":
        return self.filter(registration_code=registration_code).first()
