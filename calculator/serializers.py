from rest_framework import serializers
from django.contrib.auth.models import User

from calculator.models import UserCalculationHistory


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email','password']

class UserCalculationHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model= UserCalculationHistory
        fields=['id','user','expression','result','Created_at']
