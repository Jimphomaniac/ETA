import io
import logging
import csv
import sklearn
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.template import loader
from django.urls import reverse
from sklearn.naive_bayes import MultinomialNB

from .forms import CreateUserForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
import csv
from django.shortcuts import render
from .forms import UploadCSVForm
from MajorProject.predict import make_prediction


def index(request):
    if request.user.is_authenticated:
        return redirect('home')
    return render(request, "index.html", {})


@login_required(login_url="login")
def home(request):
    return render(request, "home.html", {'navbar': 'home'})


@login_required(login_url="login")
def dashboard(request):
    return render(request, "dashboard.html", {'navbar': 'dashboard'})


def loginForm(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        authUser = authenticate(request, username=username, password=password)

        if authUser is not None:
            login(request, authUser)
            return redirect('home')
        else:
            messages.info(request, "It seems you entered an incorrect name or password!")

    return render(request, "login.html", {'navbar': 'login'})


def register(request):
    form = CreateUserForm()
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = CreateUserForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, 'Welcome ' + username + ', your account has been created please log in to '
                                                              'continue.')
            return redirect('login')

    return render(request, "register.html", {'form': form, 'navbar': 'register'})


@login_required(login_url="login")
def logoutMethod(request):
    logout(request)
    return redirect('login')


@login_required(login_url="login")
def csv_upload(request):
    data = []
    if request.method == 'POST':
        print("Uploading!!!")
        form = UploadCSVForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file']
            decoded_file = csv_file.read().decode('utf-8').splitlines()
            reader = csv.reader(decoded_file)
            for row in reader:
                data.append(row)
    else:
        form = UploadCSVForm()

    # Make Predictions
    data, raw_data = make_prediction(data)

    print("Predictions Complete")
    return render(request, 'dashboard.html', {'form': form, 'data': data, 'raw_data': raw_data})


