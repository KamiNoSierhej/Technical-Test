from rest_framework import serializers
from users.models import User, Profile, CreditCheck
from phonenumber_field.serializerfields import PhoneNumberField
from rest_auth.registration.serializers import RegisterSerializer


class CustomRegisterSerializer(RegisterSerializer):
    username = None


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email',)


class CreditCheckSerializer(serializers.ModelSerializer):
    accepted = serializers.BooleanField(read_only=True)
    data = serializers.JSONField(read_only=True)

    class Meta:
        model = CreditCheck
        fields = ('accepted', 'data',)


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
