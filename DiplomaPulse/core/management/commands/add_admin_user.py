from django.core.management.base import BaseCommand, CommandError
from django.utils.crypto import get_random_string

from accounts.models.base_user import BaseUser
from DiplomaPulse.settings import DEBUG

EMAIL = "admin@mail.com"
PASSWORD = get_random_string(length=12)


class Command(BaseCommand):
	help = "This command allows to create an admin user for local deployment"

	def handle(self, *args, **kwargs):
		if not DEBUG:
			raise CommandError("Cannot use this command in PROD mode for safety reasons")

		try:
			BaseUser.objects.create_superuser(
				email=EMAIL,
				password=PASSWORD,
			)
		except Exception as e:
			self.stdout.write(self.style.ERROR(f"Couldn't create a user: {e=}"))
			exit(0)

		self.stdout.write(self.style.SUCCESS(f"Created a superuser with {EMAIL=} and {PASSWORD=}"))
