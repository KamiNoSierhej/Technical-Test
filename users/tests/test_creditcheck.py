import mock

from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate

from users.models import User, Profile, CreditCheck
from users.views.credit_check import CreditCheckView

factory = APIRequestFactory()


class CreditCheckViewTest(TestCase):

    def setUp(self):
        self.user = User(email='test@test.test')
        self.user.save()
        self.profile = Profile(
            first_name='Tommy', last_name='Wiseau', user=self.user
        )
        self.profile.save()
        self.credit_check_error = {'Message': 'error'}
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

    @mock.patch('users.serializers.credit_check.credit_check_call')
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

    @mock.patch('users.serializers.credit_check.credit_check_call')
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

    @mock.patch('users.serializers.credit_check.credit_check_call')
    def test_default_behaviour_error(self, credit_check):
        credit_check.return_value = self.credit_check_error
        request = factory.post('/', data={}, format='json')
        force_authenticate(request, self.user)

        response = self.view(request)

        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
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
        self.assertFalse(
            CreditCheck.objects.filter(user_id=self.user.id).exists()
        )

    def test_retrieve(self):
        CreditCheck(user=self.user).save()
        request = factory.get('/', format='json')
        force_authenticate(request, self.user)

        response = self.view(request)

        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_retrieve_when_no_credit_check(self):
        request = factory.get('/', format='json')
        force_authenticate(request, self.user)

        response = self.view(request)

        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_destroy(self):
        CreditCheck(user=self.user).save()
        request = factory.delete('/', format='json')
        force_authenticate(request, self.user)

        response = self.view(request)

        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_destroy_when_no_credit_check(self):
        request = factory.delete('/', format='json')
        force_authenticate(request, self.user)

        response = self.view(request)

        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)

    @property
    def view(self):
        return CreditCheckView.as_view(
            {
                'get': 'retrieve',
                'post': 'create',
                'put': 'update',
                'delete': 'destroy'
            }
        )
