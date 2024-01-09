import os

from django.contrib.auth.hashers import make_password
from django.template.loader import render_to_string
from dotenv import load_dotenv
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from django.conf import settings
from django.core.mail import EmailMessage, get_connection


# Create your views here.
class LoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        # Standartverhalten für die ObtainAuthToken-Klasse
        serializer = self.serializer_class(data=request.data,
                                           context={"request": request})
        try:
            serializer.is_valid(raise_exception=True)
        except Exception:
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
        }, status=status.HTTP_200_OK)


class RegisterView(APIView):
    @staticmethod
    def post(request):
        load_dotenv()

        email = request.data.get("email")
        name = request.data.get("name")
        password = request.data.get("password")

        if email and name and password:
            # Überprüfen, ob der Benutzer bereits existiert
            if User.objects.filter(email=email).exists():
                return Response({"status": 401, "message": "Email already in use"}, status=status.HTTP_401_UNAUTHORIZED)

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

            template = render_to_string('registration.html', {'name': name})

            with get_connection(
                    host=settings.RESEND_SMTP_HOST,
                    port=settings.RESEND_SMTP_PORT,
                    username=settings.RESEND_SMTP_USERNAME,
                    password=os.environ["RESEND_API_KEY"],
                    use_tls=True,
            ) as connection:
                r = EmailMessage(
                    subject="Registration",
                    body=template,
                    to=[email],
                    from_email="join@daniel-rubin.de",
                    connection=connection).send()

            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            return Response({"status": 401, "message": "Something went wrong"}, status=status.HTTP_401_UNAUTHORIZED)


# class ResetPasswordView(APIView):
#     @staticmethod
#     def post(request):
#         email = request.data.get("email")
#
#         if User.objects.filter(email=email).exists():
#             # Senden der Reset-Passwort-E-Mail an den User
#             send_mail(
#                 'Reset Password',
#                 'Please follow the instructions to reset your password.',
#                 'contact@daniel-rubin.de',  # Absender-E-Mail-Adresse
#                 [email],  # Empfänger-E-Mail-Adresse
#                 fail_silently=False,
#                 auth_user='m06624d4',
#                 auth_password='3Y9kJcKSxBPgZp9ZT6aY'
#             )
#
#         return Response(status=status.HTTP_200_OK)
