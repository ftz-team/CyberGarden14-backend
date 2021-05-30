from django.conf.urls import url, include
from django.urls import path

from .views import *

api_urls = [
    url(r'^rest-auth/', include('rest_auth.urls')),
    url(r'^rest-auth/registration/', include('rest_auth.registration.urls')),

    path('auth', Auth.as_view(), name='auth'),
    path('auth/code', AuthCode.as_view(), name='auth_code'),

    path('collector/create', CreateCollectorView.as_view(), name='create_collector'),
    path('collector/get', GetCollectorsView.as_view(), name='get_collectors'),
    path('collector/detailed', GetDetailedCollectorView.as_view(), name='get_detailed'),

    path('collector/add_to_favourites', AddCollectorToFavourites.as_view(), name='add_to_favourites'),
    path('collector/get_favourites', GetFavouriteCollectors.as_view(), name='get_favourites'),


    path('contact/create', CreateContactView.as_view(), name='create_contact'),

    path('visit/create', CreateVisit.as_view(), name='create_visit'),
    path('visit/history', GetUsersHistory.as_view(), name='users_history'),
    
    path('users_history/get', GetUsersHistory.as_view(), name='get_users_history'),
    path('promotion/get', GetPromotions.as_view(), name='get_promo'),

    path('achivements/get', GetUsersAchievements.as_view(), name='get_achievements'),
]

