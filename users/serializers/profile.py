from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers

from django.conf import settings
from users.models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(
        required=False, allow_blank=True, max_length=100
    )
    last_name = serializers.CharField(
        required=False, allow_blank=True, max_length=100
    )
    date_of_birth = serializers.DateField(
        required=False,
        allow_null=True,
        format=settings.DATE_FORMATS,
        input_formats=settings.DATE_INPUT_FORMATS
    )
    mobile_phone = PhoneNumberField(required=False, allow_blank=True)
    user = serializers.HiddenField(
        allow_null=False, default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Profile
        fields = (
            'first_name',
            'last_name',
            'date_of_birth',
            'mobile_phone',
            'user'
        )
