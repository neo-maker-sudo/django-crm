"""crm URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, reverse_lazy
from django.contrib.auth.views import (
    LoginView, LogoutView,
    PasswordResetDoneView,
    PasswordResetCompleteView,
)
from base import views as base_views

urlpatterns = [
    path('admin', admin.site.urls),
    path("leads/", include("leads.urls")),
    path("agents/", include("agents.urls", namespace="agents")),
    path("categories/", include("category.urls")),
    path("payment/", include("payment.urls")),
    path("punching/", include("punching.urls")),
    path("meeting/", include("meeting.urls")),
    path("login", base_views.CustomLoginView.as_view(), name="login"),
    path("logout", LogoutView.as_view(
        next_page=reverse_lazy("login"),
    ), name="logout"),

    path("password/change", base_views.PasswordChangeView.as_view(), name="password_change"),
    path('password/reset', base_views.CustomPasswordResetView.as_view(),name='password_reset'),
    path('password/reset/done', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path("password/reset/confirm/<uidb64>/<token>/", base_views.CustomPasswordConfirmView.as_view(), name="password_reset_confirm"),
    path('password/reset/complete', PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    path("", base_views.LandingPageView.as_view(), name="landing"),
    path("signup", base_views.SignUpView.as_view(), name="signup"),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)