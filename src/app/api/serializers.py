from rest_framework import serializers
from core.models import *


class VisitSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Visit


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Contact


class CollectorSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Collector
