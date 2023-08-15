from django.urls import path

from .views import ContactsView, UserView

urlpatterns = [
    path('', ContactsView.as_view(), name="Contacts"),
]
