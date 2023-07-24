from django.urls import path

from .views import ContactsView, UserView

urlpatterns = [
    path('', ContactsView.as_view(), name="Contacts"),
    path('<int:pk>/', UserView.as_view(), name='User'),
]
