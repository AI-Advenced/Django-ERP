from django.urls import path
from . import views

app_name = 'projects'

urlpatterns = [
    # Dashboard
    path('', views.ProjectDashboardView.as_view(), name='dashboard'),
    
    # Projects
    path('projects/', views.ProjectListView.as_view(), name='project_list'),
    path('projects/create/', views.ProjectCreateView.as_view(), name='project_create'),
    path('projects/<int:pk>/', views.ProjectDetailView.as_view(), name='project_detail'),
    path('projects/<int:pk>/edit/', views.ProjectUpdateView.as_view(), name='project_update'),
    path('projects/<int:pk>/delete/', views.ProjectDeleteView.as_view(), name='project_delete'),
    
    # Tasks
    path('tasks/', views.TaskListView.as_view(), name='task_list'),
    path('tasks/create/', views.TaskCreateView.as_view(), name='task_create'),
    path('tasks/<int:pk>/', views.TaskDetailView.as_view(), name='task_detail'),
    path('tasks/<int:pk>/edit/', views.TaskUpdateView.as_view(), name='task_update'),
    path('tasks/<int:pk>/delete/', views.TaskDeleteView.as_view(), name='task_delete'),
    
    # Milestones
    path('milestones/', views.MilestoneListView.as_view(), name='milestone_list'),
    path('milestones/create/', views.MilestoneCreateView.as_view(), name='milestone_create'),
    path('milestones/<int:pk>/', views.MilestoneDetailView.as_view(), name='milestone_detail'),
    path('milestones/<int:pk>/edit/', views.MilestoneUpdateView.as_view(), name='milestone_update'),
    path('milestones/<int:pk>/delete/', views.MilestoneDeleteView.as_view(), name='milestone_delete'),
    
    # Time Entries
    path('time-entries/', views.TimeEntryListView.as_view(), name='timeentry_list'),
    path('time-entries/create/', views.TimeEntryCreateView.as_view(), name='timeentry_create'),
]
