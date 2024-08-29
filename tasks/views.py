from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import TaskForm
from .models import Task
from django.utils import timezone
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
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=True)
    return render(request, 'tasks.html', {
        'tasks' : tasks
    })

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
            new_task.user = request.user
            new_task.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'create_task.html', {
            'form' : TaskForm,
            'error': 'Please provide valide data'
        })

#TASK DETAILS
def task_detail(request, task_id):
    if request.method == 'GET':
        task = get_object_or_404(Task, pk=task_id, user=request.user)
        form = TaskForm(instance=task)
        return render(request, 'task_detail.html', {'task': task, 'form': form})
    else:
        try:
            task = get_object_or_404(Task, pk=task_id, user=request.user)
            form = TaskForm(request.POST, instance=task)
            form.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'task_detail.html', {'task': task, 'form': form, 'error': 'Error updating task'})

#COMPLETE TASK
def complete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.datecompleted = timezone.now()
        task.save()
        return redirect('tasks')

#DELETE TASK
def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.datecompleted = timezone.now()
        task.delete()
        return redirect('tasks')

#TASKS COMPLETEDS
def tasks_completed(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted') 
    return render(request, 'tasks_completed.html', {
        'tasks' : tasks
    })


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