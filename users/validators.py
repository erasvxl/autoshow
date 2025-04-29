from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

class CustomMinLengthValidator:
    def __init__(self, min_length=8):
        self.min_length = min_length

    def validate(self, password, user=None):
        if len(password) < self.min_length:
            raise ValidationError(
                _(f"Пароль должен содержать не менее {self.min_length} символов."),
                code='password_too_short',
            )

    def get_help_text(self):
        return f"Пароль должен содержать не менее {self.min_length} символов."
