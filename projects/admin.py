from django.contrib import admin
from .models import Project, Task, Milestone, TimeEntry, ProjectDocument


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'status', 'priority', 'manager', 'start_date', 'end_date', 'progress', 'is_active']
    list_filter = ['status', 'priority', 'is_active', 'start_date']
    search_fields = ['name', 'code', 'client_name', 'description']
    filter_horizontal = ['team_members']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'start_date'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'code', 'description', 'status', 'priority', 'is_active')
        }),
        ('Dates', {
            'fields': ('start_date', 'end_date', 'actual_start_date', 'actual_end_date')
        }),
        ('Budget', {
            'fields': ('estimated_budget', 'actual_budget')
        }),
        ('Progress', {
            'fields': ('progress',)
        }),
        ('Team', {
            'fields': ('manager', 'team_members')
        }),
        ('Client Information', {
            'fields': ('client_name', 'client_contact', 'client_email')
        }),
        ('Additional Information', {
            'fields': ('notes',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'project', 'status', 'priority', 'assigned_to', 'due_date', 'progress']
    list_filter = ['status', 'priority', 'project']
    search_fields = ['title', 'description', 'project__name']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'due_date'
    filter_horizontal = ['depends_on']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('project', 'title', 'description', 'status', 'priority')
        }),
        ('Assignment', {
            'fields': ('assigned_to',)
        }),
        ('Dates', {
            'fields': ('start_date', 'due_date', 'completed_date')
        }),
        ('Effort', {
            'fields': ('estimated_hours', 'actual_hours', 'progress')
        }),
        ('Dependencies', {
            'fields': ('depends_on',)
        }),
        ('Additional Information', {
            'fields': ('notes',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Milestone)
class MilestoneAdmin(admin.ModelAdmin):
    list_display = ['name', 'project', 'status', 'due_date', 'completed_date']
    list_filter = ['status', 'project']
    search_fields = ['name', 'description', 'project__name']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'due_date'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('project', 'name', 'description', 'status')
        }),
        ('Dates', {
            'fields': ('due_date', 'completed_date')
        }),
        ('Deliverables', {
            'fields': ('deliverables',)
        }),
        ('Additional Information', {
            'fields': ('notes',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(TimeEntry)
class TimeEntryAdmin(admin.ModelAdmin):
    list_display = ['user', 'task', 'date', 'hours']
    list_filter = ['date', 'user', 'task__project']
    search_fields = ['task__title', 'user__username', 'description']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'date'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('task', 'user', 'date', 'hours')
        }),
        ('Description', {
            'fields': ('description',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(ProjectDocument)
class ProjectDocumentAdmin(admin.ModelAdmin):
    list_display = ['title', 'project', 'uploaded_by', 'created_at']
    list_filter = ['project', 'created_at']
    search_fields = ['title', 'description', 'project__name']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('project', 'title', 'description', 'file', 'uploaded_by')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
