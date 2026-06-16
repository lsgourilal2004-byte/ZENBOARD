from django.shortcuts import render, redirect, get_object_or_404
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
def project_create(request):
    if request.method == 'POST':
        name = request.POST['name']
        description = request.POST.get('description', '')
        Project.objects.create(name=name, description=description, owner=request.user)
        return redirect('project_list')
    return render(request, 'tasks/project_form.html', {'action': 'Create'})

@login_required
def project_edit(request, pk):
    project = get_object_or_404(Project, id=pk, owner=request.user)
    if request.method == 'POST':
        project.name = request.POST['name']
        project.description = request.POST.get('description', '')
        project.save()
        return redirect('project_list')
    return render(request, 'tasks/project_form.html', {'action': 'Edit', 'project': project})

@login_required
def project_delete(request, pk):
    project = get_object_or_404(Project, id=pk, owner=request.user)
    if request.method == 'POST':
        project.delete()
        return redirect('project_list')
    return render(request, 'tasks/project_confirm_delete.html', {'project': project})

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
@login_required
def task_create(request):
    projects = Project.objects.filter(owner=request.user)
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST.get('description', '')
        status = request.POST.get('status', 'todo')
        priority = request.POST.get('priority', 'medium')
        project_id = request.POST['project']
        deadline = request.POST.get('deadline') or None
        project = get_object_or_404(Project, id=project_id, owner=request.user)
        Task.objects.create(
            title=title,
            description=description,
            status=status,
            priority=priority,
            project=project,
            deadline=deadline
        )
        return redirect('task_list')
    return render(request, 'tasks/task_form.html', {'action': 'Create', 'projects': projects})

@login_required
def task_edit(request, pk):
    task = get_object_or_404(Task, id=pk, project__owner=request.user)
    projects = Project.objects.filter(owner=request.user)
    if request.method == 'POST':
        task.title = request.POST['title']
        task.description = request.POST.get('description', '')
        task.status = request.POST.get('status', 'todo')
        task.priority = request.POST.get('priority', 'medium')
        task.deadline = request.POST.get('deadline') or None
        task.project = get_object_or_404(Project, id=request.POST['project'], owner=request.user)
        task.save()
        return redirect('task_list')
    return render(request, 'tasks/task_form.html', {'action': 'Edit', 'task': task, 'projects': projects})

@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, id=pk, project__owner=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('task_list')
    return render(request, 'tasks/task_confirm_delete.html', {'task': task})