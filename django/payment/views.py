from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, View
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.urls import reverse
import stripe


class CheckoutView(View):
    def get(self, request, *args, **kwargs):
        price = 2000
        context = {
            "product": "test product",
            "price": price
        }
        return render(request, "payment/stripe/checkout.html", context)

    def post(self, request, *args, **kwargs):
        name = request.POST.get("name")
        price = request.POST.get("price")

        stripe.api_key = settings.STRIPE_SECRET_KEY

        try:
            checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                        "price_data": {
                            "unit_amount": price,
                            "currency": "usd",
                            "product_data": {
                                "name": name,
                                
                            }
                        },
                        "quantity": 1,
                    }
                ],
                mode="payment",
                success_url=request.build_absolute_uri(reverse("stripe_checkout_success")),
                cancel_url=request.build_absolute_uri(reverse("stripe_checkout_cancel"))
            )
        except Exception as e:
            raise e
        
        return redirect(checkout_session.url)


def checkout_success_view(request):

    context = {
        
    }
    return render(request, "payment/stripe/success.html", context)


def checkout_cancel_view(request):

    context = {
        
    }
    return render(request, "payment/stripe/cancel.html", context)


@csrf_exempt
def stripe_webhook_view(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
        print(event, payload)
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # 判斷事件 update database

    # Passed signature verification
    return HttpResponse(status=200)
