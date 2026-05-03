from django.apps import AppConfig
from django.db.utils import OperationalError, ProgrammingError


class UsersConfig(AppConfig):
    name = "users"

    def ready(self):
        from .models import User
        from core.bloom import email_bloom

        try:
            for email in User.objects.values_list("email", flat=True):
                email_bloom.add(email)
        except (OperationalError, ProgrammingError):
            # DB not ready yet → skip
            pass