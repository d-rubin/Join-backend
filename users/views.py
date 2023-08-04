from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


# Create your views here.
class ContactsView(ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
