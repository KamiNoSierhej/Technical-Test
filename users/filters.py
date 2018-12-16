from rest_framework.filters import BaseFilterBackend


class RetrieveForLoggedUserFilter(BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        return queryset.filter(user_id=request.user.id)
