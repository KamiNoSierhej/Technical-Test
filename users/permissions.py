from rest_framework.permissions import BasePermission


class CompletedSignupAndAcceptedCredit(BasePermission):
    """
    Only user who has filled the whole profile got accepted for
    credit has access.
    """

    def has_permission(self, request, view):
        logged_user = request.user

        return (
            logged_user.has_profile and
            logged_user.has_creditcheck and
            logged_user.creditcheck.accepted and
            logged_user.profile.completed
        )
