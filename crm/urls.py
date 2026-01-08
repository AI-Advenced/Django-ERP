from django.urls import path
from . import views

app_name = 'crm'

urlpatterns = [
    # Lead URLs
    path('leads/', views.LeadListView.as_view(), name='lead_list'),
    path('leads/create/', views.LeadCreateView.as_view(), name='lead_create'),
    path('leads/<int:pk>/', views.LeadDetailView.as_view(), name='lead_detail'),
    path('leads/<int:pk>/edit/', views.LeadUpdateView.as_view(), name='lead_update'),
    path('leads/<int:pk>/delete/', views.LeadDeleteView.as_view(), name='lead_delete'),
    
    # Contact URLs
    path('contacts/', views.ContactListView.as_view(), name='contact_list'),
    path('contacts/create/', views.ContactCreateView.as_view(), name='contact_create'),
    path('contacts/<int:pk>/', views.ContactDetailView.as_view(), name='contact_detail'),
    path('contacts/<int:pk>/edit/', views.ContactUpdateView.as_view(), name='contact_update'),
    path('contacts/<int:pk>/delete/', views.ContactDeleteView.as_view(), name='contact_delete'),
    
    # Opportunity URLs
    path('opportunities/', views.OpportunityListView.as_view(), name='opportunity_list'),
    path('opportunities/create/', views.OpportunityCreateView.as_view(), name='opportunity_create'),
    path('opportunities/<int:pk>/', views.OpportunityDetailView.as_view(), name='opportunity_detail'),
    path('opportunities/<int:pk>/edit/', views.OpportunityUpdateView.as_view(), name='opportunity_update'),
    path('opportunities/<int:pk>/delete/', views.OpportunityDeleteView.as_view(), name='opportunity_delete'),
    
    # Activity URLs
    path('activities/', views.ActivityListView.as_view(), name='activity_list'),
    path('activities/create/', views.ActivityCreateView.as_view(), name='activity_create'),
    path('activities/<int:pk>/', views.ActivityDetailView.as_view(), name='activity_detail'),
    path('activities/<int:pk>/edit/', views.ActivityUpdateView.as_view(), name='activity_update'),
    path('activities/<int:pk>/delete/', views.ActivityDeleteView.as_view(), name='activity_delete'),
]
