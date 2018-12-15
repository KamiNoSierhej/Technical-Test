from mock import Mock

from datetime import datetime
from django.test import TestCase

from users.permissions import CompletedSignupAndAcceptedCredit
from users.models import User, Profile, CreditCheck


class CompletedSignupAndAcceptedCreditTest(TestCase):

    def setUp(self):
        self.user = User(email='test@test.test')
        self.user.save()
        self.profile = Profile(
            first_name='Tommy',
            last_name='Wiseau',
            date_of_birth=datetime.now().date(),
            mobile_phone='+48691070500',
            user=self.user

        )
        self.profile.save()
        self.credit_check = CreditCheck(
            user=self.user,
            accepted=True,
        )
        self.credit_check.save()
        self.fake_request = Mock(user=self.user)

    def test_user_with_accepted_credit_check_and_filed_profile(self):
        access = CompletedSignupAndAcceptedCredit.has_permission(
            None, self.fake_request, None
        )

        self.assertTrue(access)

    def test_user_with_rejected_credit_check_and_filed_profile(self):
        self.credit_check.accepted = False
        self.credit_check.save()

        access = CompletedSignupAndAcceptedCredit.has_permission(
            None, self.fake_request, None
        )

        self.assertFalse(access)

    def test_user_with_rejected_credit_check_and_incomplete_profile(self):
        self.credit_check.accepted = False
        self.credit_check.save()
        self.profile.last_name = None
        self.profile.save()

        access = CompletedSignupAndAcceptedCredit.has_permission(
            None, self.fake_request, None
        )

        self.assertFalse(access)

    def test_user_with_accepted_credit_check_and_incomplete_profile(self):
        self.profile.last_name = None
        self.profile.save()

        access = CompletedSignupAndAcceptedCredit.has_permission(
            None, self.fake_request, None
        )

        self.assertFalse(access)

    def test_user_with_accepted_credit_check_without_profile(self):
        self.profile.delete()

        access = CompletedSignupAndAcceptedCredit.has_permission(
            None, self.fake_request, None
        )

        self.assertFalse(access)

    def test_user_without_profile_and_credit_check(self):
        self.profile.delete()
        self.credit_check.delete()

        access = CompletedSignupAndAcceptedCredit.has_permission(
            None, self.fake_request, None
        )

        self.assertFalse(access)
