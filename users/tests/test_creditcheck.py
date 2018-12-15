import mock

from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate

from users.models import User, Profile, CreditCheck
from users.views import CreditCheckCreationView

factory = APIRequestFactory()


class CreditCheckCreationViewTest(TestCase):

    def setUp(self):
        self.user = User(email='test@test.test')
        self.user.save()
        self.profile = Profile(
            first_name='Tommy', last_name='Wiseau', user=self.user
        )
        self.profile.save()
        self.credit_check_error = {'message': 'error'}
        self.credit_check_accepted = {
            'name': 'Tommy Wiseau',
            'accepted': True
        }
        self.credit_check_rejected = {
            'name': 'Tommy Wiseau',
            'accepted': False
        }

    def test_unauthorized_user(self):
        request = factory.post('/', data={}, format='json')

        response = self.view(request)

        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertFalse(
            CreditCheck.objects.filter(user_id=self.user.id).exists()
        )

    @mock.patch('users.views.credit_check')
    def test_default_behaviour_accepted(self, credit_check):
        credit_check.return_value = self.credit_check_accepted
        request = factory.post('/', data={}, format='json')
        force_authenticate(request, self.user)

        response = self.view(request)

        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertDictEqual(
            response.data, {'accepted': True, 'user': self.user.id}
        )
        self.assertTrue(
            CreditCheck.objects.filter(user_id=self.user.id).exists()
        )

    @mock.patch('users.views.credit_check')
    def test_default_behaviour_rejected(self, credit_check):
        credit_check.return_value = self.credit_check_rejected
        request = factory.post('/', data={}, format='json')
        force_authenticate(request, self.user)

        response = self.view(request)

        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertDictEqual(
            response.data, {'accepted': False, 'user': self.user.id}
        )
        self.assertTrue(
            CreditCheck.objects.filter(user_id=self.user.id).exists()
        )

    @mock.patch('users.views.credit_check')
    def test_default_behaviour_error(self, credit_check):
        credit_check.return_value = self.credit_check_error
        request = factory.post('/', data={}, format='json')
        force_authenticate(request, self.user)

        response = self.view(request)

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(response.data, {'message': 'error'})
        self.assertFalse(
            CreditCheck.objects.filter(user_id=self.user.id).exists()
        )

    def test_user_with_no_profile(self):
        self.profile.delete()
        self.user.refresh_from_db()
        request = factory.post('/', data={}, format='json')
        force_authenticate(request, self.user)

        response = self.view(request)

        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertDictEqual(
            response.data, {'message': 'Users first or last name missing.'}
        )
        self.assertFalse(
            CreditCheck.objects.filter(user_id=self.user.id).exists()
        )

    @property
    def view(self):
        return CreditCheckCreationView.as_view()
