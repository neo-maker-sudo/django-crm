from django.urls import path
from . import views

urlpatterns = [
    path("", views.PunchingLandingPage.as_view(), name="punching_landing"),
]
