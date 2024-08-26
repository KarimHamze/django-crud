from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm

# Create your views here.

def hello(request):
    return HttpResponse(f'Hello World')

def signup(request):
    return render(request, 'signup.html', {
        'form': UserCreationForm
    })

