from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import user_passes_test
from .utils import generate_room_name


@user_passes_test(lambda user: user.is_active, login_url=reverse_lazy("login"))
def chat_entrance_view(request):
    
    if request.method == "POST":
        
        room_name = generate_room_name()        
        return redirect(reverse("room",  kwargs={"room_name": room_name}))
    
    context = {}
    return render(request, "meeting/entrance.html", context)


@user_passes_test(lambda user: user.is_active, login_url=reverse_lazy("login"))
def room_view(request, room_name):
    context = {
        "room_name": room_name,
    }
    return render(request, "meeting/room.html", context)