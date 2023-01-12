from django.urls import path
from . import views


urlpatterns = [
    path("checkout",views.CheckoutView.as_view(), name="stripe_checkout"),
    path("success", views.checkout_success_view, name="stripe_checkout_success"),
    path("cancel", views.checkout_cancel_view, name="stripe_checkout_cancel"),
    path("stripe/webhook", views.stripe_webhook_view, name="stripe_webhook"),
]
