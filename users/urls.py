from django.conf.urls import url

from users.views import UserListView, ProfileCreationView, CreditCheckCreationView

urlpatterns = [
    url(r'^list/$', UserListView.as_view(), name='list'),
    url(
        r'^profile/$',
        ProfileCreationView.as_view({'post': 'create'}),
        name='profile',
    ),
    url(
        r'^credit-check/$',
        CreditCheckCreationView.as_view(),
        name='credit-check',
    ),
]
