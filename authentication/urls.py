from django.urls import path, include

from .views import LoginView, RegisterView

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("register/", RegisterView.as_view(), name="register"),
    # path("reset-password/", ResetPasswordView.as_view(), name="reset-password"),
]
