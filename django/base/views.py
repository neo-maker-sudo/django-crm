from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from .forms import SignUpForm, CustomPasswordResetForm, CustomPasswordConfirmForm, LoginForm, CustomPasswordChangeForm
from django.views.generic import TemplateView, CreateView
from django.contrib.auth.views import (
    PasswordResetView, PasswordResetConfirmView, LoginView, PasswordChangeView
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

class PasswordChangeView(PasswordChangeView):
    template_name: str = "registration/password_change.html"
    form_class = CustomPasswordChangeForm
    success_url = reverse_lazy("punching_landing")

    def form_valid(self, form):
        return super().form_valid(form)


class CustomPasswordResetView(PasswordResetView):
    form_class = CustomPasswordResetForm


class CustomPasswordConfirmView(PasswordResetConfirmView):
    form_class = CustomPasswordConfirmForm
