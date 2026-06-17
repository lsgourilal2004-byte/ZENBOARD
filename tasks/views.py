from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import Project, Task, PomodoroSession, UserProfile
from rest_framework import generics, permissions
from .serializers import ProjectSerializer, TaskSerializer

def home(request):
    features = [
        {'icon': '📋', 'title': 'Task Manager', 'description': 'Create, organize, and track tasks with priorities and deadlines.'},
        {'icon': '🗂️', 'title': 'Kanban Board', 'description': 'Visualize workflow with drag-and-drop cards.'},
        {'icon': '🍅', 'title': 'Pomodoro Timer', 'description': 'Stay focused with 25-min sessions and 5-min breaks.'},
        {'icon': '⚡', 'title': 'XP & Gamification', 'description': 'Earn XP for completing tasks and level up.'},
        {'icon': '📊', 'title': 'Dashboard Charts', 'description': 'Visualize your productivity with beautiful charts.'},
        {'icon': '🔒', 'title': 'Secure & Private', 'description': 'Built with Django\'s secure authentication system.'},
    ]
    return render(request, 'tasks/home.html', {'features': features})

def about(request):
    tech_stack = ['Python & Django', 'Django REST Framework', 'SQLite', 'HTML5 / CSS3 / Tailwind', 'JavaScript', 'Git & GitHub']
    features = ['Task Management (CRUD)', 'Kanban Board', 'Pomodoro Timer', 'REST API', 'Dashboard Charts', 'XP Gamification']
    return render(request, 'tasks/about.html', {'tech_stack': tech_stack, 'features': features})

@login_required
def dashboard(request):
    projects = Project.objects.filter(owner=request.user)
    tasks = Task.objects.filter(project__owner=request.user)
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    context = {
        'projects': projects,
        'tasks': tasks,
        'total_projects': projects.count(),
        'total_tasks': tasks.count(),
        'completed_tasks': tasks.filter(status='done').count(),
        'todo_tasks': tasks.filter(status='todo').count(),
        'inprogress_tasks': tasks.filter(status='inprogress').count(),
        'high': tasks.filter(priority='high').count(),
        'medium': tasks.filter(priority='medium').count(),
        'low': tasks.filter(priority='low').count(),
        'xp': profile.xp,
        'level': profile.level,
        'xp_progress': (profile.xp % 100),
    }
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
        # Add XP when task is done
        if task.status == 'done':
            profile, created = UserProfile.objects.get_or_create(user=request.user)
            profile.add_xp(10)
        
        return redirect('task_list')
        return redirect('task_list')
    return render(request, 'tasks/task_form.html', {'action': 'Edit', 'task': task, 'projects': projects})

@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, id=pk, project__owner=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('task_list')
    return render(request, 'tasks/task_confirm_delete.html', {'task': task})
# API Views
class ProjectListCreateAPI(generics.ListCreateAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Project.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class ProjectDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Project.objects.filter(owner=self.request.user)

class TaskListCreateAPI(generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(project__owner=self.request.user)

class TaskDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(project__owner=self.request.user)
def get_queryset(self):
        return Task.objects.filter(project__owner=self.request.user)


@login_required
def kanban(request):
    todo_tasks = Task.objects.filter(project__owner=request.user, status='todo')
    inprogress_tasks = Task.objects.filter(project__owner=request.user, status='inprogress')
    done_tasks = Task.objects.filter(project__owner=request.user, status='done')
    context = {
        'todo_tasks': todo_tasks,
        'inprogress_tasks': inprogress_tasks,
        'done_tasks': done_tasks,
    }
    return render(request, 'tasks/kanban.html', context)
    

def pomodoro(request):
    tasks = Task.objects.filter(assigned_to=request.user)
    sessions = PomodoroSession.objects.filter(user=request.user).order_by('-created_at')[:5]
    return render(request, 'tasks/pomodoro.html', {'tasks': tasks, 'sessions': sessions})

def save_pomodoro(request):
    if request.method == 'POST':
        task_id = request.POST.get('task_id')
        completed = request.POST.get('completed') == 'true'
        task = Task.objects.get(id=task_id) if task_id else None
        PomodoroSession.objects.create(
            user=request.user,
            task=task,
            completed=completed
        )
        return JsonResponse({'status': 'saved'})
        