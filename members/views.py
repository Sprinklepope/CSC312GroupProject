from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import RegisterForm
from booking.models import Ticket_History


def index(request):
    Ticket_History.objects.filter(paid=False).delete()
    return render(request, "home/home.html")


def register(response):
    if response.method == "POST":
        form = RegisterForm(response.POST)
        if form.is_valid():
            form.save()
            return redirect("/")

    else:
        form = RegisterForm()

    return render(response, "register/register.html", {"form": form})
