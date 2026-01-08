from django.db import models
from django.urls import reverse
from django.utils import timezone
from decimal import Decimal
from django.conf import settings

class Project(models.Model):
    """
    Project model for managing projects
    """
    STATUS_CHOICES = [
        ('planning', 'Planning'),
        ('in_progress', 'In Progress'),
        ('on_hold', 'On Hold'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ]
    
    name = models.CharField(max_length=200, help_text='Project name')
    code = models.CharField(max_length=50, unique=True, help_text='Unique project code')
    description = models.TextField(blank=True, help_text='Project description')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='planning')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium')
    
    # Dates
    start_date = models.DateField()
    end_date = models.DateField()
    actual_start_date = models.DateField(null=True, blank=True)
    actual_end_date = models.DateField(null=True, blank=True)
    
    # Budget
    estimated_budget = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    actual_budget = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    
    # Progress
    progress = models.IntegerField(default=0, help_text='Progress percentage (0-100)')
    
    # Team
    manager = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='managed_projects',
        help_text='Project manager'
    )

    team_members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='projects',
        blank=True,
        help_text='Project team members'
    )
    
    # Client information
    client_name = models.CharField(max_length=200, blank=True)
    client_contact = models.CharField(max_length=200, blank=True)
    client_email = models.EmailField(blank=True)
    
    # Additional info
    notes = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Project'
        verbose_name_plural = 'Projects'
    
    def __str__(self):
        return f"{self.code} - {self.name}"
    
    def get_absolute_url(self):
        return reverse('projects:project_detail', kwargs={'pk': self.pk})
    
    @property
    def is_overdue(self):
        if self.status not in ['completed', 'cancelled']:
            return timezone.now().date() > self.end_date
        return False
    
    @property
    def days_remaining(self):
        if self.status not in ['completed', 'cancelled']:
            delta = self.end_date - timezone.now().date()
            return delta.days
        return 0
    
    @property
    def budget_variance(self):
        return self.estimated_budget - self.actual_budget
    
    @property
    def tasks_count(self):
        return self.tasks.count()
    
    @property
    def completed_tasks_count(self):
        return self.tasks.filter(status='completed').count()
    
    @property
    def task_completion_rate(self):
        total = self.tasks_count
        if total > 0:
            return (self.completed_tasks_count / total) * 100
        return 0


class Task(models.Model):
    """
    Task model for project tasks
    """
    STATUS_CHOICES = [
        ('todo', 'To Do'),
        ('in_progress', 'In Progress'),
        ('review', 'In Review'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ]
    
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='tasks',
        help_text='Associated project'
    )
    title = models.CharField(max_length=200, help_text='Task title')
    description = models.TextField(blank=True, help_text='Task description')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='todo')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium')
    
    # Assignment
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_tasks',
        help_text='Team member assigned to this task'
    )
    
    # Dates
    start_date = models.DateField(null=True, blank=True)
    due_date = models.DateField()
    completed_date = models.DateField(null=True, blank=True)
    
    # Effort
    estimated_hours = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=0,
        help_text='Estimated hours to complete'
    )
    actual_hours = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=0,
        help_text='Actual hours spent'
    )
    
    # Progress
    progress = models.IntegerField(default=0, help_text='Task progress (0-100)')
    
    # Dependencies
    depends_on = models.ManyToManyField(
        'self',
        symmetrical=False,
        blank=True,
        related_name='dependent_tasks',
        help_text='Tasks that must be completed before this task'
    )
    
    # Additional info
    notes = models.TextField(blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['due_date', '-priority']
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'
    
    def __str__(self):
        return f"{self.project.code} - {self.title}"
    
    def get_absolute_url(self):
        return reverse('projects:task_detail', kwargs={'pk': self.pk})
    
    @property
    def is_overdue(self):
        if self.status not in ['completed', 'cancelled']:
            return timezone.now().date() > self.due_date
        return False
    
    @property
    def days_remaining(self):
        if self.status not in ['completed', 'cancelled']:
            delta = self.due_date - timezone.now().date()
            return delta.days
        return 0


class Milestone(models.Model):
    """
    Milestone model for project milestones
    """
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('missed', 'Missed'),
    ]
    
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='milestones',
        help_text='Associated project'
    )
    name = models.CharField(max_length=200, help_text='Milestone name')
    description = models.TextField(blank=True, help_text='Milestone description')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Dates
    due_date = models.DateField()
    completed_date = models.DateField(null=True, blank=True)
    
    # Deliverables
    deliverables = models.TextField(blank=True, help_text='Expected deliverables')
    
    # Additional info
    notes = models.TextField(blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['due_date']
        verbose_name = 'Milestone'
        verbose_name_plural = 'Milestones'
    
    def __str__(self):
        return f"{self.project.code} - {self.name}"
    
    def get_absolute_url(self):
        return reverse('projects:milestone_detail', kwargs={'pk': self.pk})
    
    @property
    def is_overdue(self):
        if self.status not in ['completed']:
            return timezone.now().date() > self.due_date
        return False


class TimeEntry(models.Model):
    """
    Time entry model for tracking time spent on tasks
    """
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name='time_entries',
        help_text='Associated task'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='time_entries',
        help_text='User who logged the time'
    )
    date = models.DateField(default=timezone.now)
    hours = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        help_text='Hours spent'
    )
    description = models.TextField(blank=True, help_text='Work description')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-date', '-created_at']
        verbose_name = 'Time Entry'
        verbose_name_plural = 'Time Entries'
    
    def __str__(self):
        return f"{self.user.username} - {self.task.title} - {self.hours}h"
    
    def get_absolute_url(self):
        return reverse('projects:timeentry_detail', kwargs={'pk': self.pk})


class ProjectDocument(models.Model):
    """
    Project document model for storing project-related documents
    """
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='documents',
        help_text='Associated project'
    )
    title = models.CharField(max_length=200, help_text='Document title')
    description = models.TextField(blank=True, help_text='Document description')
    file = models.FileField(upload_to='project_documents/', help_text='Document file')
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='uploaded_documents',
        help_text='User who uploaded the document'
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Project Document'
        verbose_name_plural = 'Project Documents'
    
    def __str__(self):
        return f"{self.project.code} - {self.title}"
    
    def get_absolute_url(self):
        return reverse('projects:document_detail', kwargs={'pk': self.pk})
