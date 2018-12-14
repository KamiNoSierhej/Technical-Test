from django.conf.urls import url

from signup.views import UserListView, ProfileCreationView

urlpatterns = [
    url(r'^users/$', UserListView.as_view(), name='users'),
    url(
        r'^profile/$',
        ProfileCreationView.as_view({'post': 'create'}),
        name='profile',
    ),
]
