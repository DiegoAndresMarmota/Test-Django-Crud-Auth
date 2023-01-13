from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import TaskForm

# from django.views.decorators.csrf import csrf_protect

# Create your views here.
# @csrf_protect

def home(request):
    return render(request, 'home.html')

def signup(request):
    
    if request.method == 'GET':
        return render(request, 'signup.html', {
        'form': UserCreationForm
    })
    else:
        if request.POST['password1'] == request.POST['password2']:
            #Registrar usuario
            try:
                user = User.objects.create_user(username=request.POST['username'], password = request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('tasks')
            except IntegrityError:
                return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    "error": "Usuario ya existe"
                })
        return render(request, 'signup.html', {
            'form': UserCreationForm,
            "error": "Contraseña no coincide"
        })
        
def tasks(request):
    return render(request, 'tasks.html', {
        'form': TaskForm
    })

def create_tasks(request):
    if request.method == 'GET':
        return render(request, 'create_task.html', {
            'form': TaskForm
        })
    else:
        return render(request, 'create_task.html', {
            'form': TaskForm
        })
        

def signout(request):
    logout(request)
    return redirect('home')

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
                'error': 'El usuario o la contraseña son incorrectas'
            })
        else:
            login(request, user)
            return redirect('tasks')