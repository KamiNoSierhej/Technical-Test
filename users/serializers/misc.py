from rest_framework import serializers
from rest_auth.registration.serializers import RegisterSerializer
from rest_auth.serializers import LoginSerializer


class CustomRegisterSerializer(RegisterSerializer):
    username = serializers.CharField(read_only=True)


class CustomLoginSerializer(LoginSerializer):
    username = serializers.CharField(read_only=True)
