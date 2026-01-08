"""
Business Intelligence & Reporting Views
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Sum, Avg, Q
from django.utils import timezone
from datetime import timedelta
import json

from .models import (
    DataSource, Dashboard, KPI, KPIHistory,
    Report, ReportExecution, Widget
)
from .forms import (
    DataSourceForm, DashboardForm, KPIForm, KPIHistoryForm,
    ReportForm, WidgetForm
)


# ==================== Main Analytics Dashboard ====================

@login_required
def analytics_dashboard(request):
    """Main Business Intelligence Dashboard"""
    
    # Get user's default dashboard or create one
    default_dashboard = Dashboard.objects.filter(
        Q(owner=request.user) | Q(shared_with=request.user),
        is_default=True
    ).first()
    
    # KPI Summary
    active_kpis = KPI.objects.filter(is_active=True, show_on_dashboard=True)
    
    # KPIs by category
    kpis_by_category = {}
    for category in ['financial', 'sales', 'operations', 'quality', 'hr', 'customer']:
        kpis_by_category[category] = active_kpis.filter(category=category)[:4]
    
    # Recent Reports
    recent_reports = Report.objects.filter(
        Q(created_by=request.user) | Q(recipients=request.user)
    ).distinct()[:5]
    
    # Dashboard stats
    total_dashboards = Dashboard.objects.filter(
        Q(owner=request.user) | Q(shared_with=request.user)
    ).count()
    
    total_kpis = active_kpis.count()
    
    # KPI Status Summary
    kpi_status_summary = {
        'good': active_kpis.filter(trend='up').count(),
        'warning': 0,
        'critical': 0,
    }
    
    for kpi in active_kpis:
        if kpi.status == 'warning':
            kpi_status_summary['warning'] += 1
        elif kpi.status == 'critical':
            kpi_status_summary['critical'] += 1
    
    # Recent report executions
    recent_executions = ReportExecution.objects.filter(
        triggered_by=request.user
    ).order_by('-started_at')[:5]
    
    context = {
        'default_dashboard': default_dashboard,
        'kpis_by_category': kpis_by_category,
        'recent_reports': recent_reports,
        'total_dashboards': total_dashboards,
        'total_kpis': total_kpis,
        'kpi_status_summary': kpi_status_summary,
        'recent_executions': recent_executions,
    }
    
    return render(request, 'bi_reporting/analytics_dashboard.html', context)


# ==================== Dashboard Views ====================

@login_required
def dashboard_list(request):
    """List all dashboards"""
    dashboards = Dashboard.objects.filter(
        Q(owner=request.user) | Q(shared_with=request.user) | Q(visibility='public')
    ).distinct()
    
    # Filter by visibility
    visibility_filter = request.GET.get('visibility')
    if visibility_filter:
        dashboards = dashboards.filter(visibility=visibility_filter)
    
    context = {
        'dashboards': dashboards,
        'visibility_filter': visibility_filter,
    }
    return render(request, 'bi_reporting/dashboard_list.html', context)


@login_required
def dashboard_view(request, pk):
    """View a specific dashboard"""
    dashboard = get_object_or_404(Dashboard, pk=pk)
    
    # Check access
    if dashboard.visibility == 'private' and dashboard.owner != request.user:
        messages.error(request, 'You do not have permission to view this dashboard.')
        return redirect('bi_reporting:dashboard_list')
    
    context = {
        'dashboard': dashboard,
    }
    return render(request, 'bi_reporting/dashboard_view.html', context)


@login_required
def dashboard_create(request):
    """Create new dashboard"""
    if request.method == 'POST':
        form = DashboardForm(request.POST)
        if form.is_valid():
            dashboard = form.save(commit=False)
            dashboard.owner = request.user
            dashboard.save()
            form.save_m2m()
            messages.success(request, f'Dashboard "{dashboard.name}" created successfully!')
            return redirect('bi_reporting:dashboard_view', pk=dashboard.pk)
    else:
        form = DashboardForm()
    
    context = {'form': form}
    return render(request, 'bi_reporting/dashboard_form.html', context)


@login_required
def dashboard_update(request, pk):
    """Update dashboard"""
    dashboard = get_object_or_404(Dashboard, pk=pk, owner=request.user)
    
    if request.method == 'POST':
        form = DashboardForm(request.POST, instance=dashboard)
        if form.is_valid():
            form.save()
            messages.success(request, 'Dashboard updated successfully!')
            return redirect('bi_reporting:dashboard_view', pk=dashboard.pk)
    else:
        form = DashboardForm(instance=dashboard)
    
    context = {
        'form': form,
        'dashboard': dashboard,
    }
    return render(request, 'bi_reporting/dashboard_form.html', context)


@login_required
def dashboard_delete(request, pk):
    """Delete dashboard"""
    dashboard = get_object_or_404(Dashboard, pk=pk, owner=request.user)
    
    if request.method == 'POST':
        dashboard.delete()
        messages.success(request, 'Dashboard deleted successfully!')
        return redirect('bi_reporting:dashboard_list')
    
    context = {'dashboard': dashboard}
    return render(request, 'bi_reporting/dashboard_confirm_delete.html', context)


# ==================== KPI Views ====================

@login_required
def kpi_list(request):
    """List all KPIs"""
    kpis = KPI.objects.filter(is_active=True)
    
    # Filter by category
    category_filter = request.GET.get('category')
    if category_filter:
        kpis = kpis.filter(category=category_filter)
    
    # Search
    search_query = request.GET.get('search')
    if search_query:
        kpis = kpis.filter(
            Q(name__icontains=search_query) |
            Q(code__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    context = {
        'kpis': kpis,
        'category_filter': category_filter,
        'search_query': search_query,
    }
    return render(request, 'bi_reporting/kpi_list.html', context)


@login_required
def kpi_detail(request, pk):
    """View KPI details with history"""
    kpi = get_object_or_404(KPI, pk=pk)
    
    # Get historical data
    history = KPIHistory.objects.filter(kpi=kpi).order_by('-period_end')[:30]
    
    context = {
        'kpi': kpi,
        'history': history,
    }
    return render(request, 'bi_reporting/kpi_detail.html', context)


@login_required
def kpi_create(request):
    """Create new KPI"""
    if request.method == 'POST':
        form = KPIForm(request.POST)
        if form.is_valid():
            kpi = form.save(commit=False)
            kpi.created_by = request.user
            kpi.save()
            messages.success(request, f'KPI "{kpi.name}" created successfully!')
            return redirect('bi_reporting:kpi_detail', pk=kpi.pk)
    else:
        form = KPIForm()
    
    context = {'form': form}
    return render(request, 'bi_reporting/kpi_form.html', context)


@login_required
def kpi_update(request, pk):
    """Update KPI"""
    kpi = get_object_or_404(KPI, pk=pk)
    
    if request.method == 'POST':
        form = KPIForm(request.POST, instance=kpi)
        if form.is_valid():
            form.save()
            messages.success(request, 'KPI updated successfully!')
            return redirect('bi_reporting:kpi_detail', pk=kpi.pk)
    else:
        form = KPIForm(instance=kpi)
    
    context = {
        'form': form,
        'kpi': kpi,
    }
    return render(request, 'bi_reporting/kpi_form.html', context)


@login_required
def kpi_delete(request, pk):
    """Delete KPI"""
    kpi = get_object_or_404(KPI, pk=pk)
    
    if request.method == 'POST':
        kpi.delete()
        messages.success(request, 'KPI deleted successfully!')
        return redirect('bi_reporting:kpi_list')
    
    context = {'kpi': kpi}
    return render(request, 'bi_reporting/kpi_confirm_delete.html', context)


# ==================== Report Views ====================

@login_required
def report_list(request):
    """List all reports"""
    reports = Report.objects.filter(
        Q(created_by=request.user) | Q(recipients=request.user)
    ).distinct()
    
    # Filter by type
    type_filter = request.GET.get('type')
    if type_filter:
        reports = reports.filter(report_type=type_filter)
    
    # Filter by status
    status_filter = request.GET.get('status')
    if status_filter:
        reports = reports.filter(status=status_filter)
    
    context = {
        'reports': reports,
        'type_filter': type_filter,
        'status_filter': status_filter,
    }
    return render(request, 'bi_reporting/report_list.html', context)


@login_required
def report_detail(request, pk):
    """View report details"""
    report = get_object_or_404(Report, pk=pk)
    
    # Get execution history
    executions = ReportExecution.objects.filter(report=report).order_by('-started_at')[:10]
    
    context = {
        'report': report,
        'executions': executions,
    }
    return render(request, 'bi_reporting/report_detail.html', context)


@login_required
def report_create(request):
    """Create new report"""
    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.created_by = request.user
            report.save()
            form.save_m2m()
            messages.success(request, f'Report "{report.name}" created successfully!')
            return redirect('bi_reporting:report_detail', pk=report.pk)
    else:
        form = ReportForm()
    
    context = {'form': form}
    return render(request, 'bi_reporting/report_form.html', context)


@login_required
def report_update(request, pk):
    """Update report"""
    report = get_object_or_404(Report, pk=pk, created_by=request.user)
    
    if request.method == 'POST':
        form = ReportForm(request.POST, instance=report)
        if form.is_valid():
            form.save()
            messages.success(request, 'Report updated successfully!')
            return redirect('bi_reporting:report_detail', pk=report.pk)
    else:
        form = ReportForm(instance=report)
    
    context = {
        'form': form,
        'report': report,
    }
    return render(request, 'bi_reporting/report_form.html', context)


@login_required
def report_delete(request, pk):
    """Delete report"""
    report = get_object_or_404(Report, pk=pk, created_by=request.user)
    
    if request.method == 'POST':
        report.delete()
        messages.success(request, 'Report deleted successfully!')
        return redirect('bi_reporting:report_list')
    
    context = {'report': report}
    return render(request, 'bi_reporting/report_confirm_delete.html', context)


# ==================== Data Source Views ====================

@login_required
def datasource_list(request):
    """List all data sources"""
    datasources = DataSource.objects.all()
    
    context = {
        'datasources': datasources,
    }
    return render(request, 'bi_reporting/datasource_list.html', context)


@login_required
def datasource_create(request):
    """Create new data source"""
    if request.method == 'POST':
        form = DataSourceForm(request.POST)
        if form.is_valid():
            datasource = form.save(commit=False)
            datasource.created_by = request.user
            datasource.save()
            messages.success(request, f'Data source "{datasource.name}" created successfully!')
            return redirect('bi_reporting:datasource_list')
    else:
        form = DataSourceForm()
    
    context = {'form': form}
    return render(request, 'bi_reporting/datasource_form.html', context)


@login_required
def datasource_update(request, pk):
    """Update data source"""
    datasource = get_object_or_404(DataSource, pk=pk)
    
    if request.method == 'POST':
        form = DataSourceForm(request.POST, instance=datasource)
        if form.is_valid():
            form.save()
            messages.success(request, 'Data source updated successfully!')
            return redirect('bi_reporting:datasource_list')
    else:
        form = DataSourceForm(instance=datasource)
    
    context = {
        'form': form,
        'datasource': datasource,
    }
    return render(request, 'bi_reporting/datasource_form.html', context)


@login_required
def datasource_delete(request, pk):
    """Delete data source"""
    datasource = get_object_or_404(DataSource, pk=pk)
    
    if request.method == 'POST':
        datasource.delete()
        messages.success(request, 'Data source deleted successfully!')
        return redirect('bi_reporting:datasource_list')
    
    context = {'datasource': datasource}
    return render(request, 'bi_reporting/datasource_confirm_delete.html', context)
