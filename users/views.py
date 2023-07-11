from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from .serializers import UserSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


# Create your views here.
class ContactsView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
