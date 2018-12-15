from datetime import datetime
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate

from users.models import User, Profile
from users.views import ProfileCreationView

factory = APIRequestFactory()


class ProfileModelTest(TestCase):

    def setUp(self):
        self.user = User(email='test@test.test')
        self.user.save()

    def test_completed_parameter_profile_filled(self):
        profile = Profile(
            first_name='first_name',
            last_name='last_name',
            date_of_birth=datetime.now().date(),
            mobile_phone='+48691070500',
            user=self.user

        )
        profile.save()

        self.assertTrue(profile.completed)

    def test_completed_parameter_profile_incompleted(self):
        profile = Profile(
            first_name='first_name',
            date_of_birth=datetime.now().date(),
            mobile_phone='+48691070500',
            user=self.user

        )
        profile.save()

        self.assertFalse(profile.completed)


class ProfileCreationViewTest(TestCase):

    def setUp(self):
        self.user = User(email='test@test.test')
        self.user.save()
        self.full_request_data = {
            'first_name': 'Tommy',
            'last_name': 'Wiseau',
            'date_of_birth': '10-10-1979',
            'mobile_phone': '+48691070500',
        }

    def test_unauthorized_user(self):
        request = factory.post('/', data={}, format='json')

        response = self.view(request)

        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertFalse(Profile.objects.filter(user_id=self.user.id).exists())

    def test_no_data_prvided(self):
        request = factory.post('/', data={}, format='json')
        force_authenticate(request, self.user)

        self.assertFalse(Profile.objects.filter(user_id=self.user.id).exists())

        response = self.view(request)

        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertDictEqual(
            response.data,
            {
                'first_name': None,
                'last_name': None,
                'date_of_birth': None,
                'mobile_phone': None,
                'user': self.user.id
            }
        )
        self.assertTrue(Profile.objects.filter(user_id=self.user.id).exists())

    def test_full_data_prvided(self):
        request = factory.post('/', data=self.full_request_data, format='json')
        force_authenticate(request, self.user)

        response = self.view(request)

        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertDictEqual(
            response.data,
            {
                'first_name': 'Tommy',
                'last_name': 'Wiseau',
                'date_of_birth': '10-10-1979',
                'mobile_phone': '+48691070500',
                'user': self.user.id
            }
        )
        self.assertTrue(Profile.objects.filter(user_id=self.user.id).exists())

    def test_full_data_prvided_then_one_field_edited(self):
        request = factory.post('/', data=self.full_request_data, format='json')
        force_authenticate(request, self.user)

        response = self.view(request)

        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertDictEqual(
            response.data,
            {
                'first_name': 'Tommy',
                'last_name': 'Wiseau',
                'date_of_birth': '10-10-1979',
                'mobile_phone': '+48691070500',
                'user': self.user.id
            }
        )

        profile_id = self.user.profile.id
        request_data = {'mobile_phone': '+48500075887'}
        request = factory.post('/', data=request_data, format='json')
        force_authenticate(request, self.user)

        response = self.view(request)

        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertDictEqual(
            response.data,
            {
                'first_name': 'Tommy',
                'last_name': 'Wiseau',
                'date_of_birth': '10-10-1979',
                'mobile_phone': '+48500075887',
                'user': self.user.id
            }
        )
        self.assertEquals(self.user.profile.id, profile_id)

    def test_invalid_data_prvided(self):
        request_data = {
            'mobile_phone': '+4887',
            'date_of_birth': '01/01/2000',
        }
        request = factory.post('/', data=request_data, format='json')
        force_authenticate(request, self.user)

        response = self.view(request)

        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            str(*response.data['date_of_birth']),
            'Date has wrong format. Use one of these formats instead:'
            ' DD-MM-YYYY, YYYY-MM-DD.'
        )
        self.assertEqual(
            str(*response.data['mobile_phone']),
            'Enter a valid phone number.'
        )
        self.assertEqual(len(response.data), 2)
        self.assertFalse(Profile.objects.filter(user_id=self.user.id).exists())

    @property
    def view(self):
        return ProfileCreationView.as_view({'post': 'create'})