from django.conf.urls import url

from users.views.user import UserListView
from users.views.profile import ProfileView
from users.views.credit_check import CreditCheckView

urlpatterns = [
    url(r'^list/$', UserListView.as_view({'get': 'list'}), name='list'),
    url(
        r'^profile/$',
        ProfileView.as_view(
            {
                'get': 'retrieve',
                'post': 'create',
                'patch': 'partial_update',
                'delete': 'destroy'
            }
        ),
        name='profile',
    ),
    url(
        r'^credit-check/$',
        CreditCheckView.as_view(
            {
                'get': 'retrieve',
                'post': 'create',
                'put': 'update',
                'delete': 'destroy'
            }
        ),
        name='credit-check',
    ),
]
