from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.db import IntegrityError
# Create your views here.

# HOME WEBSITE
def home(request):
    return render(request, 'home.html')

# SIGN-UP WEBSITE
def signup(request):

    if request.method == 'GET':
        return render(request, 'signup.html', {
        'form': UserCreationForm
    })
    else:
        if request.POST['password1'] == request.POST['password2']:
            #Register user
            try:
                user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('tasks')
            except IntegrityError:
                return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    'error': 'Username already exist'
                 })
        else:
            return render(request, 'signup.html', {
                        'form': UserCreationForm,
                        'error': 'Password do not match'
                          })

#TASK WEBSITE
def tasks(request):
    return render(request, 'tasks.html')

