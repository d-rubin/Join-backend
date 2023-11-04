from django.contrib.auth.models import User
from rest_framework.generics import ListCreateAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK

from .serializers import UserSerializer


# Create your views here.
class ContactsView(ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def retrieve(self, request, *args, **kwargs):
        user_data = {
            'username': request.user.username,
            'email': request.user.email,  # Oder andere Benutzerattribute, die Sie zurückgeben möchten
        }
        return Response(user_data, status=HTTP_200_OK)
