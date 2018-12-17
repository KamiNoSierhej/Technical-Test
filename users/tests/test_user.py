from django.test import TestCase

from users.models import User, Profile, CreditCheck


class UserModelTest(TestCase):

    def setUp(self):
        self.user = User(email='test@test.test')
        self.user.save()

    def test_parameter_has_profile(self):
        self.assertFalse(self.user.has_profile)

        Profile(user=self.user).save()

        self.assertTrue(self.user.has_profile)

    def test_parameter_has_creditcheck(self):
        self.assertFalse(self.user.has_creditcheck)

        CreditCheck(user=self.user).save()

        self.assertTrue(self.user.has_creditcheck)
