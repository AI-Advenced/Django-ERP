from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.db.models import Q, Count, Sum
from django.contrib import messages
from django.utils import timezone
from .models import Project, Task, Milestone, TimeEntry, ProjectDocument
from .forms import ProjectForm, TaskForm, MilestoneForm, TimeEntryForm, ProjectDocumentForm


class ProjectDashboardView(LoginRequiredMixin, ListView):
    """
    Dashboard view showing project overview and statistics
    """
    model = Project
    template_name = 'projects/dashboard.html'
    context_object_name = 'projects'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Statistics
        context['total_projects'] = Project.objects.filter(is_active=True).count()
        context['active_projects'] = Project.objects.filter(
            status='in_progress',
            is_active=True
        ).count()
        context['completed_projects'] = Project.objects.filter(
            status='completed'
        ).count()
        context['total_tasks'] = Task.objects.count()
        context['pending_tasks'] = Task.objects.filter(status='todo').count()
        context['overdue_tasks'] = Task.objects.filter(
            due_date__lt=timezone.now().date()
        ).exclude(status__in=['completed', 'cancelled']).count()
        
        # Recent projects
        context['recent_projects'] = Project.objects.filter(
            is_active=True
        )[:5]
        
        # My tasks
        if self.request.user.is_authenticated:
            context['my_tasks'] = Task.objects.filter(
                assigned_to=self.request.user
            ).exclude(status__in=['completed', 'cancelled'])[:10]
        
        # Upcoming milestones
        context['upcoming_milestones'] = Milestone.objects.filter(
            status__in=['pending', 'in_progress']
        ).order_by('due_date')[:5]
        
        return context


class ProjectListView(LoginRequiredMixin, ListView):
    """
    List view for projects
    """
    model = Project
    template_name = 'projects/project_list.html'
    context_object_name = 'projects'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = Project.objects.all()
        
        # Search
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(code__icontains=search) |
                Q(client_name__icontains=search)
            )
        
        # Filter by status
        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status=status)
        
        return queryset


class ProjectDetailView(LoginRequiredMixin, DetailView):
    """
    Detail view for a project
    """
    model = Project
    template_name = 'projects/project_detail.html'
    context_object_name = 'project'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = self.object
        
        # Tasks statistics
        context['tasks'] = project.tasks.all()[:10]
        context['total_tasks'] = project.tasks.count()
        context['completed_tasks'] = project.tasks.filter(status='completed').count()
        context['in_progress_tasks'] = project.tasks.filter(status='in_progress').count()
        context['overdue_tasks'] = project.tasks.filter(
            due_date__lt=timezone.now().date()
        ).exclude(status__in=['completed', 'cancelled']).count()
        
        # Milestones
        context['milestones'] = project.milestones.all()
        
        # Documents
        context['documents'] = project.documents.all()[:5]
        
        # Team members
        context['team_members'] = project.team_members.all()
        
        return context


class ProjectCreateView(LoginRequiredMixin, CreateView):
    """
    Create view for projects
    """
    model = Project
    form_class = ProjectForm
    template_name = 'projects/project_form.html'
    
    def form_valid(self, form):
        messages.success(self.request, 'Project created successfully!')
        return super().form_valid(form)


class ProjectUpdateView(LoginRequiredMixin, UpdateView):
    """
    Update view for projects
    """
    model = Project
    form_class = ProjectForm
    template_name = 'projects/project_form.html'
    
    def form_valid(self, form):
        messages.success(self.request, 'Project updated successfully!')
        return super().form_valid(form)


class ProjectDeleteView(LoginRequiredMixin, DeleteView):
    """
    Delete view for projects
    """
    model = Project
    template_name = 'projects/project_confirm_delete.html'
    success_url = reverse_lazy('projects:project_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Project deleted successfully!')
        return super().delete(request, *args, **kwargs)


# Task Views
class TaskListView(LoginRequiredMixin, ListView):
    """
    List view for tasks
    """
    model = Task
    template_name = 'projects/task_list.html'
    context_object_name = 'tasks'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = Task.objects.select_related('project', 'assigned_to').all()
        
        # Search
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(project__name__icontains=search)
            )
        
        # Filter by status
        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status=status)
        
        # Filter by project
        project_id = self.request.GET.get('project')
        if project_id:
            queryset = queryset.filter(project_id=project_id)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['projects'] = Project.objects.filter(is_active=True)
        return context


class TaskDetailView(LoginRequiredMixin, DetailView):
    """
    Detail view for a task
    """
    model = Task
    template_name = 'projects/task_detail.html'
    context_object_name = 'task'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        task = self.object
        
        # Time entries
        context['time_entries'] = task.time_entries.all()
        context['total_hours'] = task.time_entries.aggregate(
            total=Sum('hours')
        )['total'] or 0
        
        # Dependencies
        context['dependencies'] = task.depends_on.all()
        context['dependent_tasks'] = task.dependent_tasks.all()
        
        return context


class TaskCreateView(LoginRequiredMixin, CreateView):
    """
    Create view for tasks
    """
    model = Task
    form_class = TaskForm
    template_name = 'projects/task_form.html'
    
    def get_initial(self):
        initial = super().get_initial()
        project_id = self.request.GET.get('project')
        if project_id:
            initial['project'] = project_id
        return initial
    
    def form_valid(self, form):
        messages.success(self.request, 'Task created successfully!')
        return super().form_valid(form)


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    """
    Update view for tasks
    """
    model = Task
    form_class = TaskForm
    template_name = 'projects/task_form.html'
    
    def form_valid(self, form):
        messages.success(self.request, 'Task updated successfully!')
        return super().form_valid(form)


class TaskDeleteView(LoginRequiredMixin, DeleteView):
    """
    Delete view for tasks
    """
    model = Task
    template_name = 'projects/task_confirm_delete.html'
    success_url = reverse_lazy('projects:task_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Task deleted successfully!')
        return super().delete(request, *args, **kwargs)


# Milestone Views
class MilestoneListView(LoginRequiredMixin, ListView):
    """
    List view for milestones
    """
    model = Milestone
    template_name = 'projects/milestone_list.html'
    context_object_name = 'milestones'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = Milestone.objects.select_related('project').all()
        
        # Filter by project
        project_id = self.request.GET.get('project')
        if project_id:
            queryset = queryset.filter(project_id=project_id)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['projects'] = Project.objects.filter(is_active=True)
        return context


class MilestoneDetailView(LoginRequiredMixin, DetailView):
    """
    Detail view for a milestone
    """
    model = Milestone
    template_name = 'projects/milestone_detail.html'
    context_object_name = 'milestone'


class MilestoneCreateView(LoginRequiredMixin, CreateView):
    """
    Create view for milestones
    """
    model = Milestone
    form_class = MilestoneForm
    template_name = 'projects/milestone_form.html'
    
    def get_initial(self):
        initial = super().get_initial()
        project_id = self.request.GET.get('project')
        if project_id:
            initial['project'] = project_id
        return initial
    
    def form_valid(self, form):
        messages.success(self.request, 'Milestone created successfully!')
        return super().form_valid(form)


class MilestoneUpdateView(LoginRequiredMixin, UpdateView):
    """
    Update view for milestones
    """
    model = Milestone
    form_class = MilestoneForm
    template_name = 'projects/milestone_form.html'
    
    def form_valid(self, form):
        messages.success(self.request, 'Milestone updated successfully!')
        return super().form_valid(form)


class MilestoneDeleteView(LoginRequiredMixin, DeleteView):
    """
    Delete view for milestones
    """
    model = Milestone
    template_name = 'projects/milestone_confirm_delete.html'
    success_url = reverse_lazy('projects:milestone_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Milestone deleted successfully!')
        return super().delete(request, *args, **kwargs)


# Time Entry Views
class TimeEntryListView(LoginRequiredMixin, ListView):
    """
    List view for time entries
    """
    model = TimeEntry
    template_name = 'projects/timeentry_list.html'
    context_object_name = 'time_entries'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = TimeEntry.objects.select_related('task', 'user').all()
        
        # Filter by task
        task_id = self.request.GET.get('task')
        if task_id:
            queryset = queryset.filter(task_id=task_id)
        
        # Filter by user
        user_id = self.request.GET.get('user')
        if user_id:
            queryset = queryset.filter(user_id=user_id)
        
        return queryset


class TimeEntryCreateView(LoginRequiredMixin, CreateView):
    """
    Create view for time entries
    """
    model = TimeEntry
    form_class = TimeEntryForm
    template_name = 'projects/timeentry_form.html'
    
    def get_initial(self):
        initial = super().get_initial()
        task_id = self.request.GET.get('task')
        if task_id:
            initial['task'] = task_id
        initial['user'] = self.request.user
        return initial
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, 'Time entry created successfully!')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('projects:task_detail', kwargs={'pk': self.object.task.pk})
