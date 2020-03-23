from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from users.forms import CustomUserCreationForm

# We rename these as we have login and logout functions below
from django.contrib.auth import authenticate
from django.contrib.auth import logout as djangoLogout
from django.contrib.auth import login as djangoLogin

from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse

# Create your views here.
def register(request):
    if request.user.is_authenticated:
        return render(request, "register.html")
    else:
        if request.method == 'POST':
            form = CustomUserCreationForm(request.POST)
            if form.is_valid():
                user = form.save()
                djangoLogin(request, user)
                # return to index
                return redirect('index')
        if request.method == 'GET':
            form = CustomUserCreationForm()
            return render(request, "register.html", {'form': form})


def login(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                djangoLogin(request, user)
                return redirect('index')
            else:
                return render(request, "login.html", {'form': AuthenticationForm})
        elif request.method == 'GET':
            return render(request, "login.html", {'form': AuthenticationForm})

        

def logout(request):
    if request.user.is_authenticated:
        djangoLogout(request)
        return render(request, 'logout.html')
    else:
        return render(request, 'logout.html')