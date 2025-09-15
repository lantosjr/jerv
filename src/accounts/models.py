from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError
import re


class CustomUser(AbstractUser):
    """
    Custom user model extending Django's AbstractUser
    """
    phone_number = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        help_text="Telefonszám (nem kötelező)"
    )

    company_name = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Cég neve (nem kötelező)"
    )

    class Meta:
        verbose_name = 'Felhasználó'
        verbose_name_plural = 'Felhasználók'

    def __str__(self):
        return f"{self.username} ({self.get_full_name() or 'Nincs név'})"

    def clean(self):
        super().clean()
        # Additional validation can be added here
        if self.phone_number and not re.match(r'^\+?[\d\s\-\(\)]+$', self.phone_number):
            raise ValidationError({'phone_number': 'Érvénytelen telefonszám formátum.'})


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