"""
Quality Management Views
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Q, Avg, Sum
from django.utils import timezone
from datetime import timedelta

from .models import (
    InspectionType, Inspection, InspectionCheckpoint,
    NonConformance, CorrectiveAction
)
from .forms import (
    InspectionTypeForm, InspectionForm, InspectionCheckpointForm,
    NonConformanceForm, CorrectiveActionForm
)


# ==================== Dashboard ====================

@login_required
def quality_dashboard(request):
    """Quality Management Dashboard"""
    
    # Date ranges
    today = timezone.now().date()
    last_30_days = today - timedelta(days=30)
    
    # Inspection Statistics
    total_inspections = Inspection.objects.count()
    pending_inspections = Inspection.objects.filter(
        status__in=['scheduled', 'in_progress']
    ).count()
    passed_inspections = Inspection.objects.filter(status='passed').count()
    failed_inspections = Inspection.objects.filter(status='failed').count()
    
    # Recent Inspections
    recent_inspections = Inspection.objects.all()[:5]
    
    # Overdue Inspections
    overdue_inspections = Inspection.objects.filter(
        status__in=['scheduled', 'in_progress'],
        scheduled_date__lt=today
    )[:5]
    
    # Non-Conformance Statistics
    total_ncr = NonConformance.objects.count()
    open_ncr = NonConformance.objects.filter(
        status__in=['reported', 'investigating', 'action_required']
    ).count()
    critical_ncr = NonConformance.objects.filter(
        severity='critical',
        status__in=['reported', 'investigating', 'action_required']
    ).count()
    
    recent_ncr = NonConformance.objects.all()[:5]
    
    # CAPA Statistics
    total_capa = CorrectiveAction.objects.count()
    pending_capa = CorrectiveAction.objects.filter(
        status__in=['draft', 'pending_approval', 'approved', 'in_progress']
    ).count()
    overdue_capa = CorrectiveAction.objects.filter(
        status__in=['approved', 'in_progress'],
        target_date__lt=today
    ).count()
    
    recent_capa = CorrectiveAction.objects.all()[:5]
    
    # Monthly Trend Data (for charts)
    last_6_months = []
    for i in range(6):
        month_start = today.replace(day=1) - timedelta(days=30*i)
        last_6_months.append(month_start)
    
    inspection_trend = []
    ncr_trend = []
    for month in reversed(last_6_months):
        next_month = month + timedelta(days=32)
        next_month = next_month.replace(day=1)
        
        inspection_count = Inspection.objects.filter(
            created_at__gte=month,
            created_at__lt=next_month
        ).count()
        
        ncr_count = NonConformance.objects.filter(
            created_at__gte=month,
            created_at__lt=next_month
        ).count()
        
        inspection_trend.append({
            'month': month.strftime('%b %Y'),
            'count': inspection_count
        })
        
        ncr_trend.append({
            'month': month.strftime('%b %Y'),
            'count': ncr_count
        })
    
    context = {
        'total_inspections': total_inspections,
        'pending_inspections': pending_inspections,
        'passed_inspections': passed_inspections,
        'failed_inspections': failed_inspections,
        'recent_inspections': recent_inspections,
        'overdue_inspections': overdue_inspections,
        
        'total_ncr': total_ncr,
        'open_ncr': open_ncr,
        'critical_ncr': critical_ncr,
        'recent_ncr': recent_ncr,
        
        'total_capa': total_capa,
        'pending_capa': pending_capa,
        'overdue_capa': overdue_capa,
        'recent_capa': recent_capa,
        
        'inspection_trend': inspection_trend,
        'ncr_trend': ncr_trend,
    }
    
    return render(request, 'quality/dashboard.html', context)


# ==================== Inspection Views ====================

@login_required
def inspection_list(request):
    """List all inspections"""
    inspections = Inspection.objects.select_related(
        'inspection_type', 'inspector', 'supervisor'
    ).all()
    
    # Filtering
    status_filter = request.GET.get('status')
    if status_filter:
        inspections = inspections.filter(status=status_filter)
    
    search_query = request.GET.get('search')
    if search_query:
        inspections = inspections.filter(
            Q(inspection_number__icontains=search_query) |
            Q(title__icontains=search_query) |
            Q(reference_number__icontains=search_query)
        )
    
    context = {
        'inspections': inspections,
        'status_filter': status_filter,
        'search_query': search_query,
    }
    return render(request, 'quality/inspection_list.html', context)


@login_required
def inspection_detail(request, pk):
    """View inspection details"""
    inspection = get_object_or_404(
        Inspection.objects.select_related(
            'inspection_type', 'inspector', 'supervisor', 'created_by'
        ).prefetch_related('checkpoints', 'non_conformances'),
        pk=pk
    )
    
    context = {
        'inspection': inspection,
    }
    return render(request, 'quality/inspection_detail.html', context)


@login_required
def inspection_create(request):
    """Create new inspection"""
    if request.method == 'POST':
        form = InspectionForm(request.POST)
        if form.is_valid():
            inspection = form.save(commit=False)
            inspection.created_by = request.user
            inspection.save()
            messages.success(request, f'Inspection {inspection.inspection_number} created successfully!')
            return redirect('quality:inspection_detail', pk=inspection.pk)
    else:
        form = InspectionForm()
    
    context = {'form': form}
    return render(request, 'quality/inspection_form.html', context)


@login_required
def inspection_update(request, pk):
    """Update inspection"""
    inspection = get_object_or_404(Inspection, pk=pk)
    
    if request.method == 'POST':
        form = InspectionForm(request.POST, instance=inspection)
        if form.is_valid():
            form.save()
            messages.success(request, 'Inspection updated successfully!')
            return redirect('quality:inspection_detail', pk=inspection.pk)
    else:
        form = InspectionForm(instance=inspection)
    
    context = {
        'form': form,
        'inspection': inspection,
    }
    return render(request, 'quality/inspection_form.html', context)


@login_required
def inspection_delete(request, pk):
    """Delete inspection"""
    inspection = get_object_or_404(Inspection, pk=pk)
    
    if request.method == 'POST':
        inspection.delete()
        messages.success(request, 'Inspection deleted successfully!')
        return redirect('quality:inspection_list')
    
    context = {'inspection': inspection}
    return render(request, 'quality/inspection_confirm_delete.html', context)


# ==================== Non-Conformance Views ====================

@login_required
def nonconformance_list(request):
    """List all non-conformance reports"""
    ncrs = NonConformance.objects.select_related(
        'inspection', 'detected_by', 'assigned_to', 'created_by'
    ).all()
    
    # Filtering
    status_filter = request.GET.get('status')
    if status_filter:
        ncrs = ncrs.filter(status=status_filter)
    
    severity_filter = request.GET.get('severity')
    if severity_filter:
        ncrs = ncrs.filter(severity=severity_filter)
    
    search_query = request.GET.get('search')
    if search_query:
        ncrs = ncrs.filter(
            Q(ncr_number__icontains=search_query) |
            Q(title__icontains=search_query) |
            Q(reference_number__icontains=search_query)
        )
    
    context = {
        'ncrs': ncrs,
        'status_filter': status_filter,
        'severity_filter': severity_filter,
        'search_query': search_query,
    }
    return render(request, 'quality/nonconformance_list.html', context)


@login_required
def nonconformance_detail(request, pk):
    """View non-conformance details"""
    ncr = get_object_or_404(
        NonConformance.objects.select_related(
            'inspection', 'detected_by', 'assigned_to', 'created_by'
        ).prefetch_related('corrective_actions'),
        pk=pk
    )
    
    context = {'ncr': ncr}
    return render(request, 'quality/nonconformance_detail.html', context)


@login_required
def nonconformance_create(request):
    """Create new non-conformance report"""
    if request.method == 'POST':
        form = NonConformanceForm(request.POST)
        if form.is_valid():
            ncr = form.save(commit=False)
            ncr.created_by = request.user
            ncr.save()
            messages.success(request, f'NCR {ncr.ncr_number} created successfully!')
            return redirect('quality:nonconformance_detail', pk=ncr.pk)
    else:
        form = NonConformanceForm()
    
    context = {'form': form}
    return render(request, 'quality/nonconformance_form.html', context)


@login_required
def nonconformance_update(request, pk):
    """Update non-conformance report"""
    ncr = get_object_or_404(NonConformance, pk=pk)
    
    if request.method == 'POST':
        form = NonConformanceForm(request.POST, instance=ncr)
        if form.is_valid():
            form.save()
            messages.success(request, 'NCR updated successfully!')
            return redirect('quality:nonconformance_detail', pk=ncr.pk)
    else:
        form = NonConformanceForm(instance=ncr)
    
    context = {
        'form': form,
        'ncr': ncr,
    }
    return render(request, 'quality/nonconformance_form.html', context)


@login_required
def nonconformance_delete(request, pk):
    """Delete non-conformance report"""
    ncr = get_object_or_404(NonConformance, pk=pk)
    
    if request.method == 'POST':
        ncr.delete()
        messages.success(request, 'NCR deleted successfully!')
        return redirect('quality:nonconformance_list')
    
    context = {'ncr': ncr}
    return render(request, 'quality/nonconformance_confirm_delete.html', context)


# ==================== Corrective Action (CAPA) Views ====================

@login_required
def capa_list(request):
    """List all corrective actions"""
    capas = CorrectiveAction.objects.select_related(
        'non_conformance', 'responsible_person', 'approved_by', 'created_by'
    ).all()
    
    # Filtering
    status_filter = request.GET.get('status')
    if status_filter:
        capas = capas.filter(status=status_filter)
    
    type_filter = request.GET.get('type')
    if type_filter:
        capas = capas.filter(action_type=type_filter)
    
    search_query = request.GET.get('search')
    if search_query:
        capas = capas.filter(
            Q(capa_number__icontains=search_query) |
            Q(title__icontains=search_query)
        )
    
    context = {
        'capas': capas,
        'status_filter': status_filter,
        'type_filter': type_filter,
        'search_query': search_query,
    }
    return render(request, 'quality/capa_list.html', context)


@login_required
def capa_detail(request, pk):
    """View corrective action details"""
    capa = get_object_or_404(
        CorrectiveAction.objects.select_related(
            'non_conformance', 'responsible_person', 'approved_by', 'created_by'
        ).prefetch_related('assigned_team'),
        pk=pk
    )
    
    context = {'capa': capa}
    return render(request, 'quality/capa_detail.html', context)


@login_required
def capa_create(request):
    """Create new corrective action"""
    if request.method == 'POST':
        form = CorrectiveActionForm(request.POST)
        if form.is_valid():
            capa = form.save(commit=False)
            capa.created_by = request.user
            capa.save()
            form.save_m2m()  # Save many-to-many relationships
            messages.success(request, f'CAPA {capa.capa_number} created successfully!')
            return redirect('quality:capa_detail', pk=capa.pk)
    else:
        form = CorrectiveActionForm()
    
    context = {'form': form}
    return render(request, 'quality/capa_form.html', context)


@login_required
def capa_update(request, pk):
    """Update corrective action"""
    capa = get_object_or_404(CorrectiveAction, pk=pk)
    
    if request.method == 'POST':
        form = CorrectiveActionForm(request.POST, instance=capa)
        if form.is_valid():
            form.save()
            messages.success(request, 'CAPA updated successfully!')
            return redirect('quality:capa_detail', pk=capa.pk)
    else:
        form = CorrectiveActionForm(instance=capa)
    
    context = {
        'form': form,
        'capa': capa,
    }
    return render(request, 'quality/capa_form.html', context)


@login_required
def capa_delete(request, pk):
    """Delete corrective action"""
    capa = get_object_or_404(CorrectiveAction, pk=pk)
    
    if request.method == 'POST':
        capa.delete()
        messages.success(request, 'CAPA deleted successfully!')
        return redirect('quality:capa_list')
    
    context = {'capa': capa}
    return render(request, 'quality/capa_confirm_delete.html', context)
