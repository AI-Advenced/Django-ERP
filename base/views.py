from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count
from crm.models import Lead, Contact, Opportunity, Activity
from django.utils import timezone
from datetime import timedelta


@login_required
def index(request):
    """Dashboard view"""
    # CRM Statistics
    total_leads = Lead.objects.count()
    new_leads = Lead.objects.filter(status='new').count()
    converted_leads = Lead.objects.filter(status='converted').count()
    
    total_contacts = Contact.objects.count()
    customer_contacts = Contact.objects.filter(contact_type='customer').count()
    
    total_opportunities = Opportunity.objects.count()
    active_opportunities = Opportunity.objects.exclude(
        stage__in=['closed_won', 'closed_lost']
    ).count()
    total_opportunity_value = Opportunity.objects.aggregate(
        Sum('amount')
    )['amount__sum'] or 0
    won_opportunities = Opportunity.objects.filter(stage='closed_won').count()
    
    # Activities
    today = timezone.now().date()
    week_from_now = today + timedelta(days=7)
    
    pending_activities = Activity.objects.filter(status='planned').count()
    overdue_activities = Activity.objects.filter(
        status='planned',
        due_date__lt=timezone.now()
    ).count()
    upcoming_activities = Activity.objects.filter(
        status='planned',
        due_date__date__gte=today,
        due_date__date__lte=week_from_now
    )[:5]
    
    context = {
        'total_leads': total_leads,
        'new_leads': new_leads,
        'converted_leads': converted_leads,
        'total_contacts': total_contacts,
        'customer_contacts': customer_contacts,
        'total_opportunities': total_opportunities,
        'active_opportunities': active_opportunities,
        'total_opportunity_value': total_opportunity_value,
        'won_opportunities': won_opportunities,
        'pending_activities': pending_activities,
        'overdue_activities': overdue_activities,
        'upcoming_activities': upcoming_activities,
    }
    
    return render(request, 'base/index.html', context)
