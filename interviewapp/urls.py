from django.urls import path

from django.contrib import admin
from django.conf.urls import include, url


urlpatterns = [
    url(r'^', include('signup.urls')),
    url(r'^admin/', admin.site.urls),
    path('rest-auth/', include('rest_auth.urls')),
    path('rest-auth/registration/', include('rest_auth.registration.urls')),
]
