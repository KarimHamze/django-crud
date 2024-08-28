from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import TaskForm
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

#LOG OUT
def signout(request):
    logout(request)
    return redirect('home')

#LOG IN
def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {
        'form': AuthenticationForm
        })
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'signin.html', {
            'form': AuthenticationForm,
            'error': 'Username or password is incorrect'
            })
        else:
            login(request, user)
            return redirect('tasks')
        
#CREATE TASK
def create_task(request):
    
    if request.method == 'GET':
        return render(request, 'create_task.html', {
            'form' : TaskForm
        })
    else:
        try:
            form = TaskForm(request.POST)
            new_task = form.save(commit=False)
            new_task = request.user
            new_task.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'create_task.html', {
            'form' : TaskForm,
            'error': 'Please provide valide data'
        })