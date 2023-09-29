from django.contrib.auth.models import User
from rest_framework.generics import ListCreateAPIView
from .serializers import UserSerializer


# Create your views here.
class ContactsView(ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
