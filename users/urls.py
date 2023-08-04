from django.urls import path

from .views import ContactsView, UserView

urlpatterns = [
    path('', ContactsView.as_view(), name="Contacts"),
    path('<int:user_id>/', UserView.as_view(), name='User'),
]
