from typing import Collection
from app.settings import BASE_URL
from django.db.models.deletion import Collector
from .serializers import *
from core.models import *
from rest_framework import generics, request
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.permissions import AllowAny
from django.shortcuts import render
from rest_framework.views import APIView

class GetCollectorsView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        try:
            collectors = Collector.objects.all()
            data = []
            for collector in collectors:
                data.append({
                    'id': collector.pk,
                    'name': collector.name,
                    'lat': collector.lat,
                    'long': collector.long,
                })
            return Response({'data': data}, status=HTTP_200_OK)
        except Exception:
            return Response({'status': 'Bad Request'}, status=HTTP_400_BAD_REQUEST)


class GetUsersHistory(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        try:
            history = Visit.objects.filter(visit_user=request.user)
            data = []
            for visit in history:
                data.append({
                    'id': visit.pk,
                    'collector': visit.visit_collector.pk,
                    'date': visit.date,
                })
            return Response({'data': data}, status=HTTP_200_OK)
        except Exception:
            return Response({'status': 'Bad Request'}, status=HTTP_400_BAD_REQUEST)


class GetDetailedCollectorView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        try:
            collector = Collector.objects.filter(pk=request.GET['id'])

            try:
                _image = BASE_URL + collector.photo.url
            except Exception:
                _image = None

            data = {
                'id': collector.pk,
                'name': collector.name,
                'lat': collector.lat,
                'long': collector.long,
                'photo': _image,
                'description': collector.description,
                'contact': {
                    'phone_number': collector.collector_contact.phone_number,
                    'email': collector.collector_contact.email,
                },
                'visited_count': collector.visited_count,
            }
            return Response({'data': data}, status=HTTP_200_OK)
        except Exception:
            return Response({'status': 'Bad Request'}, status=HTTP_400_BAD_REQUEST)


class AddCollectorToFavourites(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        try:
            collector = Collector.objects.filter(pk=request.GET['id'])
            if request.GET['action'] == 'add':
                request.user.favourites.add(collector)
            if request.GET['action'] == 'remove':
                request.user.favourites.remove(collector)
            else:
                return Response({'status': 'Bad Request'}, status=HTTP_400_BAD_REQUEST)
            return Response({'status': 'OK'}, status=HTTP_200_OK)
        except Exception:
            return Response({'status': 'Bad Request'}, status=HTTP_400_BAD_REQUEST)


class GetFavouriteCollectors(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        try:
            data = []
            for collector in Collector.objects.all():
                for f in request.user.favourites():
                    if collector == f:
                        data.append({''})
            return Response({'status': data}, status=HTTP_200_OK)
        except Exception:
            return Response({'status': 'Bad Request'}, status=HTTP_400_BAD_REQUEST)


class CreateCollectorView(generics.CreateAPIView):
    queryset = Collector.objects.all()
    serializer_class = CollectorSerializer


class CreateContactView(generics.CreateAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer


