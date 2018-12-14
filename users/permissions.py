from rest_framework.permissions import BasePermission


class CompletedSignupAndAcceptedCredit(BasePermission):
    """
    Only user who has filled the whole profile got accepted for
    credit has access.
    """

    def has_permission(self, request, view):
        logged_user = request.user
        missing_profile_or_creditcheck = (
            not hasattr(logged_user, 'profile') or
            not hasattr(logged_user, 'creditcheck')
        )

        if (
            missing_profile_or_creditcheck or
            not logged_user.creditcheck.accepted or
            not logged_user.profile.completed
        ):
            return False

        return True
