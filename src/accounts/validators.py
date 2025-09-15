from django.core.exceptions import ValidationError
import re


def validate_password_strength(password):
    """
    Custom password validator for JERV ERP
    Requirements: min 8 chars, at least 1 lowercase, 1 uppercase, 1 digit
    """
    if len(password) < 8:
        raise ValidationError("A jelszónak legalább 8 karakter hosszúnak kell lennie.")

    if not re.search(r'[a-z]', password):
        raise ValidationError("A jelszónak tartalmaznia kell legalább egy kisbetűt.")

    if not re.search(r'[A-Z]', password):
        raise ValidationError("A jelszónak tartalmaznia kell legalább egy nagybetűt.")

    if not re.search(r'\d', password):
        raise ValidationError("A jelszónak tartalmaznia kell legalább egy számot.")


class CustomPasswordValidator:
    """
    Django password validator wrapper for custom validation
    """

    def validate(self, password, user=None):
        validate_password_strength(password)

    def get_help_text(self):
        return (
            "A jelszónak legalább 8 karakter hosszúnak kell lennie, "
            "és tartalmaznia kell legalább egy kisbetűt, egy nagybetűt és egy számot."
        )