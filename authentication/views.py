from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.views import APIView


# Create your views here.
class LoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        # Standartverhalten für die ObtainAuthToken-Klasse
        serializer = self.serializer_class(data=request.data,
                                           context={"request": request})
        try:
            serializer.is_valid(raise_exception=True)
        except:
            return Response({"status": 401}, status=status.HTTP_401_UNAUTHORIZED)

        user = serializer.validated_data["user"]

        # Überprüfen, ob das eingegebene Passwort übereinstimmt
        if not user.check_password(request.data.get("password")):
            return Response({"status": 401}, status=status.HTTP_401_UNAUTHORIZED)

        # Erstellen oder Abrufen des Tokens
        token, created = Token.objects.get_or_create(user=user)

        # Erstellen der Response mit dem Token
        return Response({
            "token": token.key,
            "status": 200,
        }, status=status.HTTP_201_CREATED)


class RegisterView(APIView):
    @staticmethod
    def post(request):
        email = request.data.get("email")
        name = request.data.get("name")
        password = request.data.get("password")

        if email and name and password:
            # Überprüfen, ob der Benutzer bereits existiert
            if User.objects.filter(email=email).exists():
                return Response({"status": 401}, status=status.HTTP_401_UNAUTHORIZED)

            # Überprüfen, ob der name bereits existiert
            if User.objects.filter(username=name).exists():
                return Response({"message": "Name already in use", "status": 401}, status=status.HTTP_401_UNAUTHORIZED)

            # Erstellen Sie einen neuen Benutzer mit den bereitgestellten Daten
            user = User.objects.create(
                email=email,
                username=name,
                password=make_password(password)  # Passwort hashen
            )
            user.save()

            # Token für den neu erstellten Benutzer generieren
            token, created = Token.objects.get_or_create(user=user)

            # Erstellen der Response mit dem Token
            response_data = {
                "token": token.key,
                "status": 201,
            }

            # Senden der Bestätigungs E-Mail
            send_mail(
                'Registration',
                'You have successfully registered to join, Congratulations',
                'contact@daniel-rubin.de',
                [email],
                fail_silently=False,
                auth_user='m06624d4',
                auth_password='3Y9kJcKSxBPgZp9ZT6aY'
            )

            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            return Response({"status": 401}, status=status.HTTP_401_UNAUTHORIZED)


class ResetPasswordView(APIView):
    @staticmethod
    def post(request):
        email = request.data.get("email")

        if User.objects.filter(email=email).exists():
            # Senden der Reset-Passwort-E-Mail an den User
            send_mail(
                'Reset Password',
                'Please follow the instructions to reset your password.',
                'contact@daniel-rubin.de',  # Absender-E-Mail-Adresse
                [email],  # Empfänger-E-Mail-Adresse
                fail_silently=False,
                auth_user='m06624d4',
                auth_password='3Y9kJcKSxBPgZp9ZT6aY'
            )

        return Response(status=status.HTTP_200_OK)
