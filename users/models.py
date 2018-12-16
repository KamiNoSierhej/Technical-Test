from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class User(AbstractUser):
    """Main auth user model."""

    @property
    def has_profile(self):
        try:
            self.profile
        except Profile.DoesNotExist:
            return False

        return True

    @property
    def has_creditcheck(self):
        try:
            self.creditcheck
        except CreditCheck.DoesNotExist:
            return False

        return True

    def __str__(self):
        return self.email


class Profile(models.Model):
    """User profile model. Contains private info about user."""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(null=True, blank=True, max_length=100)
    last_name = models.CharField(null=True, blank=True, max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    mobile_phone = PhoneNumberField(null=True, blank=True)

    @property
    def completed(self):
        """Returns True if all fields on profile are filled."""
        return all(
            getattr(self, field.name) for field in self._meta.local_fields
        )

    def __str__(self):
        return f'{self.user_id} Profile'


class CreditCheck(models.Model):
    """
    Model used to sore info about users credit acceptance from third
    party source.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    accepted = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user_id} CreditCheck {self.accepted}'
