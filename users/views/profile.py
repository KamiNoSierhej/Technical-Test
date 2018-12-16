from rest_framework import permissions, status
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from users.models import Profile
from users.serializers.profile import ProfileSerializer
from users.views.viewset_mixins import GetObjectMixin
from users.filters import RetrieveForLoggedUserFilter


class ProfileView(GetObjectMixin, ModelViewSet):
    """
    Logged User is able to make POST or PATCH with any of given parameters
    ('first_name', 'last_name', 'date_of_birth', 'mobile_phone') to create new
    or update already existing Profile.

    date_of_birth format: DD-MM-YYY
    mobile_phone format : dialing code and number example: "+48691060500"
    """
    model = Profile
    queryset = Profile.objects.all()
    parser_classes = (JSONParser,)
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ProfileSerializer
    filter_backends = (RetrieveForLoggedUserFilter, )

    def create(self, request, *args, **kwargs):
        if request.user.has_profile:
            return Response(
                {'message': 'User already have profile.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        return super().create(request, *args, **kwargs)
