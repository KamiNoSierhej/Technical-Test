from rest_framework import permissions, status, generics
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ViewSet

from signup.helpers import credit_check
from users.models import User, Profile, CreditCheck
from users.serializers import UserSerializer, ProfileSerializer


class UserListView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated, )


class ProfileCreationView(ModelViewSet):
    """
    Profile creation.

    Logged User is able to make POST with any of given parameters:
        'first_name', 'last_name', 'date_of_birth', 'mobile_phone'
    If there is no user Profile new one with given data will be created.
    If there is existing Profile only provided fields will be updated.
    """
    model = Profile
    parser_classes = (JSONParser,)
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = ProfileSerializer

    def create(self, request, *args, **kwargs):
        profile = Profile.objects.filter(user_id=request.user.id).first()
        serializer = self.get_serializer(profile, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )
