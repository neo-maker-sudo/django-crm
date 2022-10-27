from django.shortcuts import redirect
from django.urls import reverse
from .forms import SignUpForm, CustomPasswordResetForm, CustomPasswordConfirmForm, LoginForm
from django.views.generic import TemplateView, CreateView
from django.contrib.auth.views import (
    PasswordResetView, PasswordResetConfirmView, LoginView
)

class LandingPageView(TemplateView):
    template_name: str = "landing.html"
    

class CustomLoginView(LoginView):
    form_class = LoginForm

    def get(self, request, *args, **kwargs):
        
        if request.user.is_authenticated:
            return redirect("punching_landing")

        return super().get(request, *args, **kwargs)
    

class SignUpView(CreateView):
    template_name: str = "registration/signup.html"
    form_class = SignUpForm
    
    def get_success_url(self) -> str:
        return reverse("login")


class CustomPasswordResetView(PasswordResetView):
    form_class = CustomPasswordResetForm


class CustomPasswordConfirmView(PasswordResetConfirmView):
    form_class = CustomPasswordConfirmForm
