from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Q, Sum, Count
from django.utils import timezone
from datetime import datetime, timedelta

from .models import Lead, Contact, Opportunity, Activity


class LeadListView(LoginRequiredMixin, ListView):
    """List all leads"""
    model = Lead
    template_name = 'crm/lead_list.html'
    context_object_name = 'leads'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = Lead.objects.all()
        
        # Search functionality
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search) |
                Q(email__icontains=search) |
                Q(company__icontains=search)
            )
        
        # Filter by status
        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status=status)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status_choices'] = Lead.STATUS_CHOICES
        context['total_leads'] = Lead.objects.count()
        context['new_leads'] = Lead.objects.filter(status='new').count()
        context['converted_leads'] = Lead.objects.filter(status='converted').count()
        return context


class LeadDetailView(LoginRequiredMixin, DetailView):
    """View lead details"""
    model = Lead
    template_name = 'crm/lead_detail.html'
    context_object_name = 'lead'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['activities'] = self.object.activities.all()[:10]
        context['opportunities'] = self.object.opportunities.all()
        return context


class LeadCreateView(LoginRequiredMixin, CreateView):
    """Create new lead"""
    model = Lead
    template_name = 'crm/lead_form.html'
    fields = ['first_name', 'last_name', 'company', 'email', 'phone', 'status', 'source', 'assigned_to', 'description']
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, 'Lead created successfully!')
        return super().form_valid(form)


class LeadUpdateView(LoginRequiredMixin, UpdateView):
    """Update lead"""
    model = Lead
    template_name = 'crm/lead_form.html'
    fields = ['first_name', 'last_name', 'company', 'email', 'phone', 'status', 'source', 'assigned_to', 'description']
    
    def form_valid(self, form):
        messages.success(self.request, 'Lead updated successfully!')
        return super().form_valid(form)


class LeadDeleteView(LoginRequiredMixin, DeleteView):
    """Delete lead"""
    model = Lead
    template_name = 'crm/lead_confirm_delete.html'
    success_url = reverse_lazy('crm:lead_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Lead deleted successfully!')
        return super().delete(request, *args, **kwargs)


# Contact Views
class ContactListView(LoginRequiredMixin, ListView):
    """List all contacts"""
    model = Contact
    template_name = 'crm/contact_list.html'
    context_object_name = 'contacts'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = Contact.objects.all()
        
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search) |
                Q(email__icontains=search) |
                Q(company__icontains=search)
            )
        
        contact_type = self.request.GET.get('contact_type')
        if contact_type:
            queryset = queryset.filter(contact_type=contact_type)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['contact_type_choices'] = Contact.CONTACT_TYPE_CHOICES
        context['total_contacts'] = Contact.objects.count()
        context['customer_contacts'] = Contact.objects.filter(contact_type='customer').count()
        return context


class ContactDetailView(LoginRequiredMixin, DetailView):
    """View contact details"""
    model = Contact
    template_name = 'crm/contact_detail.html'
    context_object_name = 'contact'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['activities'] = self.object.activities.all()[:10]
        context['opportunities'] = self.object.opportunities.all()
        return context


class ContactCreateView(LoginRequiredMixin, CreateView):
    """Create new contact"""
    model = Contact
    template_name = 'crm/contact_form.html'
    fields = ['first_name', 'last_name', 'company', 'email', 'phone', 'mobile', 'contact_type', 
              'address', 'city', 'state', 'country', 'postal_code', 'assigned_to', 'notes']
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, 'Contact created successfully!')
        return super().form_valid(form)


class ContactUpdateView(LoginRequiredMixin, UpdateView):
    """Update contact"""
    model = Contact
    template_name = 'crm/contact_form.html'
    fields = ['first_name', 'last_name', 'company', 'email', 'phone', 'mobile', 'contact_type', 
              'address', 'city', 'state', 'country', 'postal_code', 'assigned_to', 'notes']
    
    def form_valid(self, form):
        messages.success(self.request, 'Contact updated successfully!')
        return super().form_valid(form)


class ContactDeleteView(LoginRequiredMixin, DeleteView):
    """Delete contact"""
    model = Contact
    template_name = 'crm/contact_confirm_delete.html'
    success_url = reverse_lazy('crm:contact_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Contact deleted successfully!')
        return super().delete(request, *args, **kwargs)


# Opportunity Views
class OpportunityListView(LoginRequiredMixin, ListView):
    """List all opportunities"""
    model = Opportunity
    template_name = 'crm/opportunity_list.html'
    context_object_name = 'opportunities'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = Opportunity.objects.select_related('contact', 'assigned_to')
        
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(contact__company__icontains=search)
            )
        
        stage = self.request.GET.get('stage')
        if stage:
            queryset = queryset.filter(stage=stage)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['stage_choices'] = Opportunity.STAGE_CHOICES
        context['total_opportunities'] = Opportunity.objects.count()
        context['total_value'] = Opportunity.objects.aggregate(Sum('amount'))['amount__sum'] or 0
        context['won_opportunities'] = Opportunity.objects.filter(stage='closed_won').count()
        context['active_opportunities'] = Opportunity.objects.exclude(
            stage__in=['closed_won', 'closed_lost']
        ).count()
        return context


class OpportunityDetailView(LoginRequiredMixin, DetailView):
    """View opportunity details"""
    model = Opportunity
    template_name = 'crm/opportunity_detail.html'
    context_object_name = 'opportunity'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['activities'] = self.object.activities.all()[:10]
        return context


class OpportunityCreateView(LoginRequiredMixin, CreateView):
    """Create new opportunity"""
    model = Opportunity
    template_name = 'crm/opportunity_form.html'
    fields = ['name', 'contact', 'lead', 'stage', 'probability', 'amount', 
              'expected_close_date', 'assigned_to', 'description']
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, 'Opportunity created successfully!')
        return super().form_valid(form)


class OpportunityUpdateView(LoginRequiredMixin, UpdateView):
    """Update opportunity"""
    model = Opportunity
    template_name = 'crm/opportunity_form.html'
    fields = ['name', 'contact', 'lead', 'stage', 'probability', 'amount', 
              'expected_close_date', 'actual_close_date', 'assigned_to', 'description']
    
    def form_valid(self, form):
        messages.success(self.request, 'Opportunity updated successfully!')
        return super().form_valid(form)


class OpportunityDeleteView(LoginRequiredMixin, DeleteView):
    """Delete opportunity"""
    model = Opportunity
    template_name = 'crm/opportunity_confirm_delete.html'
    success_url = reverse_lazy('crm:opportunity_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Opportunity deleted successfully!')
        return super().delete(request, *args, **kwargs)


# Activity Views
class ActivityListView(LoginRequiredMixin, ListView):
    """List all activities"""
    model = Activity
    template_name = 'crm/activity_list.html'
    context_object_name = 'activities'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = Activity.objects.select_related('assigned_to', 'lead', 'contact', 'opportunity')
        
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(subject__icontains=search) |
                Q(description__icontains=search)
            )
        
        activity_type = self.request.GET.get('activity_type')
        if activity_type:
            queryset = queryset.filter(activity_type=activity_type)
        
        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status=status)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['activity_type_choices'] = Activity.ACTIVITY_TYPE_CHOICES
        context['status_choices'] = Activity.STATUS_CHOICES
        context['total_activities'] = Activity.objects.count()
        context['pending_activities'] = Activity.objects.filter(status='planned').count()
        context['overdue_activities'] = Activity.objects.filter(
            status='planned',
            due_date__lt=timezone.now()
        ).count()
        return context


class ActivityDetailView(LoginRequiredMixin, DetailView):
    """View activity details"""
    model = Activity
    template_name = 'crm/activity_detail.html'
    context_object_name = 'activity'


class ActivityCreateView(LoginRequiredMixin, CreateView):
    """Create new activity"""
    model = Activity
    template_name = 'crm/activity_form.html'
    fields = ['activity_type', 'subject', 'description', 'status', 'priority', 'due_date',
              'lead', 'contact', 'opportunity', 'assigned_to']
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, 'Activity created successfully!')
        return super().form_valid(form)


class ActivityUpdateView(LoginRequiredMixin, UpdateView):
    """Update activity"""
    model = Activity
    template_name = 'crm/activity_form.html'
    fields = ['activity_type', 'subject', 'description', 'status', 'priority', 'due_date',
              'completed_date', 'lead', 'contact', 'opportunity', 'assigned_to']
    
    def form_valid(self, form):
        messages.success(self.request, 'Activity updated successfully!')
        return super().form_valid(form)


class ActivityDeleteView(LoginRequiredMixin, DeleteView):
    """Delete activity"""
    model = Activity
    template_name = 'crm/activity_confirm_delete.html'
    success_url = reverse_lazy('crm:activity_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Activity deleted successfully!')
        return super().delete(request, *args, **kwargs)
