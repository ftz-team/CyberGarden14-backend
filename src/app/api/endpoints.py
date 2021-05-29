from django.conf.urls import url, include
from django.urls import path

from .views import *

api_urls = [
    url(r'^rest-auth/', include('rest_auth.urls')),
    url(r'^rest-auth/registration/', include('rest_auth.registration.urls')),

    path('collector/create', CreateCollectorView.as_view(), name='create_collector'),
    path('contact/create', CreateContactView.as_view(), name='create_contact'),
    
    path('collector/get', GetCollectorsView.as_view(), name='get_collectors'),
    path('users_history/get', GetUsersHistory.as_view(), name='get_users_history'),
]

