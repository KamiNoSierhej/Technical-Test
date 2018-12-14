from rest_framework import permissions, status
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListCreateAPIView, CreateAPIView

from users.helpers import credit_check
from users.models import User, Profile, CreditCheck
from users.serializers import UserSerializer, ProfileSerializer, CreditCheckSerializer


class UserListView(ListCreateAPIView):
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
        profile = (
            Profile.objects.filter(user_id=request.user.id).first() or
            Profile(user=request.user)
        )
        serializer = self.get_serializer(profile, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )


class CreditCheckCreationView(CreateAPIView):
    """
    CreditCheck creation.

    User that provided first and last name of his profile is able to
    call third party provider for check for credit acceptation.
    """
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = CreditCheckSerializer

    def post(self, request, *args, **kwargs):
        logged_user = request.user
        user_without_full_name = (
            not hasattr(logged_user, 'profile') or
            (
                not logged_user.profile.first_name or
                not logged_user.profile.last_name
            )
        )

        if user_without_full_name:

            return Response(
                {'message': 'Users first or last name missing.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        credit_check_resonse = credit_check(
            logged_user.profile.first_name,
            logged_user.profile.last_name
        )
        if credit_check_resonse.get('accepted') is None:

            return Response(
                credit_check_resonse, status=status.HTTP_200_OK
            )

        if hasattr(logged_user, 'creditcheck'):
            user_credit_check = logged_user.creditcheck
            user_credit_check.accepted = credit_check_resonse['accepted']
            user_credit_check.data = credit_check_resonse
            user_credit_check.save()

            return Response(
                self.get_serializer(user_credit_check).data,
                status=status.HTTP_200_OK
            )
        else:
            user_credit_check = CreditCheck(
                user=logged_user,
                accepted=credit_check_resonse['accepted'],
                data=credit_check_resonse,
            )

            return Response(
                self.get_serializer(user_credit_check).data,
                status=status.HTTP_201_CREATED
            )
