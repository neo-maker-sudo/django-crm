from django.urls import path
from . import views

urlpatterns = [
    path("", views.chat_entrance_view, name="chat_entrance"),
    path("<str:room_name>/", views.room_view, name="room"),
]
