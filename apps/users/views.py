from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.shortcuts import render
from rest_framework.views import APIView
from users import serializers
from users.models import UserProfile

# Create your views here.


class JWTAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = serializers.JWTserializer()

