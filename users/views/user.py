from rest_framework import permissions
from rest_framework.generics import ListCreateAPIView

from users.models import User
from users.permissions import CompletedSignupAndAcceptedCredit
from users.serializers.user import UserSerializer


class UserListView(ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (
        permissions.IsAuthenticated, CompletedSignupAndAcceptedCredit
    )
