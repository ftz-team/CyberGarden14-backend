from app.settings import BASE_URL
from django.db.models.deletion import Collector
from .serializers import *
from core.models import *
from rest_framework import generics, request
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.shortcuts import render
from rest_framework.views import APIView


class Auth(APIView):
    permission_classes = (AllowAny, )

    def post(self, request):
        try:
            phone_number = request.data['phone_number']
            #send code
            return Response({'status': 'OK'}, status=HTTP_200_OK)
        except Exception:
            return Response({'status': 'Bad Request'}, status=HTTP_400_BAD_REQUEST)


class AuthCode(APIView):
    permission_classes = (AllowAny, )

    def post(self, request):
        try:
            code = request.data['code']
            if code == '1234':
                return Response({'Token': 'b532f8fe87407fb3106ee68b0e4435acf43595fe'}, status=HTTP_200_OK)
            return Response({'status': 'Bad Code'}, status=HTTP_200_OK)
        except Exception:
            return Response({'status': 'Bad Request'}, status=HTTP_400_BAD_REQUEST)


class GetCollectorsView(APIView):
    permission_classes = (IsAuthenticated,)

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
    permission_classes = (IsAuthenticated,)

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
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            collector = Collector.objects.get(id=request.GET['id'])

            try:
                _image = BASE_URL + collector.photo.url
            except Exception:
                _image = None

            data = {
                'id': collector.id,
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
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            collector = Collector.objects.get(pk=request.GET['id'])
            if request.GET['action'] == 'add':
                request.user.favourites.add(collector)
                return Response({'status': 'OK'}, status=HTTP_200_OK)
            if request.GET['action'] == 'remove':
                request.user.favourites.remove(collector)
                return Response({'status': 'OK'}, status=HTTP_200_OK)
            return Response({'status': 'Bad Request'}, status=HTTP_400_BAD_REQUEST)
        except Exception:
            return Response({'status': 'Bad Request'}, status=HTTP_400_BAD_REQUEST)


class GetFavouriteCollectors(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            data = []
            for collector in request.user.favourites.all():
                data.append({
                    'id': collector.pk,
                    'name': collector.name,
                    'lat': collector.lat,
                    'long': collector.long,
                })
            return Response({'status': data}, status=HTTP_200_OK)
        except Exception:
            return Response({'status': 'Bad Request'}, status=HTTP_400_BAD_REQUEST)


class CreateCollectorView(generics.CreateAPIView):
    queryset = Collector.objects.all()
    serializer_class = CollectorSerializer


class CreateContactView(generics.CreateAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer


class CreateVisitView(generics.CreateAPIView):
    queryset = Visit.objects.all()
    serializer_class = VisitSerializer