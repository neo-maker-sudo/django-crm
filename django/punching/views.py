from django.shortcuts import render
from django.views.generic import TemplateView


class PunchingLandingPage(TemplateView):
    template_name: str = "punching/home.html"
