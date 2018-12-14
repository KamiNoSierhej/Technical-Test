from rest_framework import serializers
from users.models import User, Profile
from phonenumber_field.serializerfields import PhoneNumberField


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email',)


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
        format='%d-%m-%Y',
        input_formats=['%d-%m-%Y', 'iso-8601']
    )
    mobile_phone = PhoneNumberField(
        required=False, allow_blank=True
    )
    user = serializers.PrimaryKeyRelatedField(
        read_only=True,
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
