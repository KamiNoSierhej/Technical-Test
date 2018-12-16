from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from users.models import CreditCheck
from users.serializers.credit_check import CreditCheckSerializer
from users.views.viewset_mixins import GetObjectMixin
from users.filters import RetrieveForLoggedUserFilter


class CreditCheckView(GetObjectMixin, ModelViewSet):
    """
    User that provided first and last name of his profile is able to
    call third party provider for check for credit acceptation.
    """
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = CreditCheckSerializer
    queryset = CreditCheck.objects.all()
    filter_backends = (RetrieveForLoggedUserFilter, )

    def create(self, request, *args, **kwargs):
        if request.user.has_creditcheck:
            return Response(
                {'message': 'User already have credit check.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        return super().create(request, *args, **kwargs)
