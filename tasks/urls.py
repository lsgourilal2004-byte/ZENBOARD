from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('projects/', views.project_list, name='project_list'),
    path('projects/create/', views.project_create, name='project_create'),
    path('projects/edit/<int:pk>/', views.project_edit, name='project_edit'),
    path('projects/delete/<int:pk>/', views.project_delete, name='project_delete'),
    path('tasks/', views.task_list, name='task_list'),

    # Tasks
    path('tasks/', views.task_list, name='task_list'),
    path('tasks/create/', views.task_create, name='task_create'),
    path('tasks/edit/<int:pk>/', views.task_edit, name='task_edit'),
    path('tasks/delete/<int:pk>/', views.task_delete, name='task_delete'),

    # Auth
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # API
    path('api/projects/', views.ProjectListCreateAPI.as_view(), name='api_projects'),
    path('api/projects/<int:pk>/', views.ProjectDetailAPI.as_view(), name='api_project_detail'),
    path('api/tasks/', views.TaskListCreateAPI.as_view(), name='api_tasks'),
    path('api/tasks/<int:pk>/', views.TaskDetailAPI.as_view(), name='api_task_detail'),
    path('Kanban/', views.kanban, name='kanban'),
    path('pomodoro/', views.pomodoro, name='pomodoro'),
     path('pomodoro/save/', views.save_pomodoro, name='save_pomodoro'),

]