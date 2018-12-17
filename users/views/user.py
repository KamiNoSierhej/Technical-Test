from rest_framework import permissions
from rest_framework.viewsets import ReadOnlyModelViewSet

from users.models import User
from users.permissions import CompletedSignupAndAcceptedCredit
from users.serializers.user import UserSerializer


class UserListView(ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (
        permissions.IsAuthenticated, CompletedSignupAndAcceptedCredit
    )
