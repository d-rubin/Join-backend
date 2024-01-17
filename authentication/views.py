from django.template.loader import render_to_string
from dotenv import load_dotenv
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from django.core.mail import send_mail


class LoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={"request": request})
        try:
            serializer.is_valid(raise_exception=True)
        except Exception:
            return Response({"status": 401}, status=status.HTTP_401_UNAUTHORIZED)

        user = serializer.validated_data["user"]

        if not user.check_password(request.data.get("password")):
            return Response({"status": 401}, status=status.HTTP_401_UNAUTHORIZED)

        token, created = Token.objects.get_or_create(user=user)

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
            if User.objects.filter(email=email).exists():
                return Response({"status": 401, "message": "Email already in use"}, status=status.HTTP_401_UNAUTHORIZED)

            if User.objects.filter(username=name).exists():
                return Response({"message": "Name already in use", "status": 401}, status=status.HTTP_401_UNAUTHORIZED)

            # user = User.objects.create(
            #     email=email,
            #     username=name,
            #     password=make_password(password)  # Passwort hashen
            # )
            # user.save()

            # token, created = Token.objects.get_or_create(user=user)

            response_data = {
                # "token": token.key,
                "status": 201,
            }

            send_mail(
                'Registration',
                'You have registered to join',
                'join@daniel-rubin.de',
                [email],
                fail_silently=False,
                html_message=render_to_string('registration.html', {'name': name})),

            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            return Response({"status": 401, "message": "Something went wrong"}, status=status.HTTP_401_UNAUTHORIZED)
