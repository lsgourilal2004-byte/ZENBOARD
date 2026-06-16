from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import Project, Task

@login_required
def dashboard(request):
    projects = Project.objects.filter(owner=request.user)
    tasks = Task.objects.filter(project__owner=request.user)
    context = {'projects': projects, 'tasks': tasks}
    return render(request, 'tasks/dashboard.html', context)

@login_required
def project_list(request):
    projects = Project.objects.filter(owner=request.user)
    return render(request, 'tasks/project_list.html', {'projects': projects})

@login_required
def task_list(request):
    tasks = Task.objects.filter(project__owner=request.user)
    return render(request, 'tasks/task_list.html', {'tasks': tasks})

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'tasks/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'tasks/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')