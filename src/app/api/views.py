from rest_framework.authtoken.models import Token
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
            if User.objects.get(username=phone_number) is None:
                user = User.objects.create_user(username=phone_number, password='secret')
                user.save()
            
            return Response({'status': 'OK'}, status=HTTP_200_OK)
        except Exception:
            return Response({'status': 'Bad Request'}, status=HTTP_400_BAD_REQUEST)


class AuthCode(APIView):
    permission_classes = (AllowAny, )

    def post(self, request):
        try:
            phone_number = request.data['phone_number']
            code = request.data['code']
            user = User.objects.get(username=phone_number)
            if code == '1234':
                return Response({'Token': str(Token.objects.get(user = user))}, status=HTTP_200_OK)
            return Response({'status': 'Bad Code'}, status=HTTP_200_OK)
        except Exception:
            return Response({'status': 'Bad Request'}, status=HTTP_400_BAD_REQUEST)


class GetCollectorsView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            type_filter = request.GET['type']

            if type_filter == 'favourites':
                collectors = request.user.favourites.all()
            if type_filter == 'all':
                collectors = Collector.objects.all()
            else:
                collectors = Collector.objects.filter(type=type_filter)

            data = []
            for collector in collectors:

                try:
                    _image = BASE_URL + collector.photo.url
                except Exception:
                    _image = None

                is_liked = collector in request.user.favourites.all()

                data.append({
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
                'type': collector.type,
                'liked': is_liked,
                'adress': collector.address,
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
            data_collector = []
            for visit in history:
                try:
                    _image = BASE_URL + visit.visit_collector.photo.url
                except Exception:
                    _image = None

                is_liked = visit.visit_collector in request.user.favourites.all()

                data_collector.append({
                    'id': visit.visit_collector.id,
                    'name': visit.visit_collector.name,
                    'lat': visit.visit_collector.lat,
                    'long': visit.visit_collector.long,
                    'photo': _image,
                    'description': visit.visit_collector.description,
                    'contact': {
                        'phone_number': visit.visit_collector.collector_contact.phone_number,
                        'email': visit.visit_collector.collector_contact.email,
                    },
                    'visited_count': visit.visit_collector.visited_count,
                    'type': visit.visit_collector.type,
                    'liked': is_liked,
                    'adress': visit.visit_collector.address,
                })

                data.append({
                    'id': visit.pk,
                    'collector': data_collector,
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

            data = []
            for collector in collectors:

                try:
                    _image = BASE_URL + collector.photo.url
                except Exception:
                    _image = None

                is_liked = collector in request.user.favourites.all()

                data.append({
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
                'type': collector.type,
                'liked': is_liked,
            })
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


class CreateVisit(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        # try:
            visit = Visit.objects.create(
                visit_user = request.user,
                visit_collector = Collector.objects.get(pk=request.data['collector_id']),
            )
            visit.save()

            to_next = 1
            next_achievement_count = 0
            achievements = list(VisitAchievement.objects.all().order_by('visit_amount'))
            for i in range(1, len(achievements)):
                if (request.user.visit_count >= achievements[i-1].visit_amount) and (request.user.visit_count < achievements[i].visit_amount):
                    to_next = achievements[i].visit_amount - request.user.visit_count
                    next_achievement_count = achievements[i].visit_amount
            
            new_achievement = False
            new_achievement_data = {}
            user_visit_count = request.user.visit_count

            for i in achievements:
                if request.user.visit_count == i.visit_amount:

                    try:
                        _image = BASE_URL + i.image.url
                    except Exception:
                        _image = None

                    new_achievement = True
                    new_achievement_data = {
                        'header': i.header,
                        'description': i.description,
                        'image': _image, 
                        'visit_amount': i.visit_amount,
                    }

            return Response({'status': 'OK', 'to_next': to_next, 'user_visit_count': user_visit_count, 'next_achievement_count': next_achievement_count, 'new_achievement': new_achievement, 'new_achievement_data': new_achievement_data}, status=HTTP_200_OK)
        # except Exception:
            return Response({'status': 'Bad Request'}, status=HTTP_400_BAD_REQUEST)