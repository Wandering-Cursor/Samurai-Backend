from django.db.models import Choices
from django.utils.translation import gettext_lazy as _


class AccountTypeChoices(Choices):
    ADMIN = "admin", _("account_type_admin")
    STUDENT = "student", _("account_type_student")
    TEACHER = "teacher", _("account_type_teacher")
    OVERSEER = "overseer", _("account_type_overseer")
