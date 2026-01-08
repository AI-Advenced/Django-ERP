from django.contrib import admin
from .models import Lead, Contact, Opportunity, Activity


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'company', 'email', 'status', 'source', 'assigned_to', 'created_at']
    list_filter = ['status', 'source', 'created_at']
    search_fields = ['first_name', 'last_name', 'email', 'company']
    date_hierarchy = 'created_at'
    raw_id_fields = ['assigned_to', 'created_by']


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'company', 'email', 'contact_type', 'assigned_to', 'created_at']
    list_filter = ['contact_type', 'created_at']
    search_fields = ['first_name', 'last_name', 'email', 'company']
    date_hierarchy = 'created_at'
    raw_id_fields = ['assigned_to', 'created_by']


@admin.register(Opportunity)
class OpportunityAdmin(admin.ModelAdmin):
    list_display = ['name', 'contact', 'stage', 'probability', 'amount', 'expected_close_date', 'assigned_to']
    list_filter = ['stage', 'probability', 'expected_close_date']
    search_fields = ['name', 'contact__first_name', 'contact__last_name', 'contact__company']
    date_hierarchy = 'expected_close_date'
    raw_id_fields = ['contact', 'lead', 'assigned_to', 'created_by']


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ['subject', 'activity_type', 'status', 'priority', 'due_date', 'assigned_to']
    list_filter = ['activity_type', 'status', 'priority', 'due_date']
    search_fields = ['subject', 'description']
    date_hierarchy = 'due_date'
    raw_id_fields = ['lead', 'contact', 'opportunity', 'assigned_to', 'created_by']
