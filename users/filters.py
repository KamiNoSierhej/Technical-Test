from rest_framework.filters import BaseFilterBackend


class RetrieveForLoggedUserFilter(BaseFilterBackend):
    """Filter out object related to logged user."""

    def filter_queryset(self, request, queryset, view):
        return queryset.filter(user_id=request.user.id)
