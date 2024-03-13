from __future__ import annotations

from typing import TYPE_CHECKING

from django.contrib.auth.models import BaseUserManager
from model_utils.managers import InheritanceManagerMixin

if TYPE_CHECKING:
    from samurai.accounts.models.base_account import BaseAccount


class BaseAccountManager(InheritanceManagerMixin, BaseUserManager):
    def create_superuser(self, email: str, password: str, **extra_fields: dict) -> BaseAccount:
        """
        Create and save a superuser with the given email and password.
        """
        user: BaseAccount = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user

    def get_user_by_registration_code(self, registration_code: str) -> BaseAccount | None:
        return self.filter(registration_code=registration_code).first()
