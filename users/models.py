from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import JSONField
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class User(AbstractUser):
    def __str__(self):
        return self.email


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(null=True, blank=True, max_length=100)
    last_name = models.CharField(null=True, blank=True, max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    mobile_phone = PhoneNumberField(null=True, blank=True)

    def __str__(self):
        return f'{self.user_id} Profile'


class CreditCheck(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    accepted = models.BooleanField(default=False)
    data = JSONField()

    def __str__(self):
        return f'{self.user_id} CreditCheck {self.accepted}'
