from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils import timezone


class Lead(models.Model):
    """
    Lead Model - Represents potential customers
    """
    STATUS_CHOICES = [
        ('new', 'New'),
        ('contacted', 'Contacted'),
        ('qualified', 'Qualified'),
        ('converted', 'Converted'),
        ('lost', 'Lost'),
    ]
    
    SOURCE_CHOICES = [
        ('website', 'Website'),
        ('referral', 'Referral'),
        ('email', 'Email Campaign'),
        ('phone', 'Phone Call'),
        ('social', 'Social Media'),
        ('other', 'Other'),
    ]
    
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    company = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    source = models.CharField(max_length=20, choices=SOURCE_CHOICES, default='other')
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_leads'
    )
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_leads'
    )
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Lead'
        verbose_name_plural = 'Leads'
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.company or 'No Company'}"
    
    def get_absolute_url(self):
        return reverse('crm:lead_detail', kwargs={'pk': self.pk})
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"


class Contact(models.Model):
    """
    Contact Model - Represents converted leads or direct contacts
    """
    CONTACT_TYPE_CHOICES = [
        ('customer', 'Customer'),
        ('supplier', 'Supplier'),
        ('partner', 'Partner'),
        ('other', 'Other'),
    ]
    
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    company = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    mobile = models.CharField(max_length=20, blank=True, null=True)
    contact_type = models.CharField(max_length=20, choices=CONTACT_TYPE_CHOICES, default='customer')
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_contacts'
    )
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_contacts'
    )
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Contact'
        verbose_name_plural = 'Contacts'
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.company or 'No Company'}"
    
    def get_absolute_url(self):
        return reverse('crm:contact_detail', kwargs={'pk': self.pk})
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"


class Opportunity(models.Model):
    """
    Opportunity Model - Sales opportunities/deals
    """
    STAGE_CHOICES = [
        ('prospecting', 'Prospecting'),
        ('qualification', 'Qualification'),
        ('proposal', 'Proposal'),
        ('negotiation', 'Negotiation'),
        ('closed_won', 'Closed Won'),
        ('closed_lost', 'Closed Lost'),
    ]
    
    PROBABILITY_CHOICES = [
        (10, '10%'),
        (25, '25%'),
        (50, '50%'),
        (75, '75%'),
        (90, '90%'),
        (100, '100%'),
    ]
    
    name = models.CharField(max_length=200)
    contact = models.ForeignKey(
        Contact,
        on_delete=models.CASCADE,
        related_name='opportunities'
    )
    lead = models.ForeignKey(
        Lead,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='opportunities'
    )
    stage = models.CharField(max_length=20, choices=STAGE_CHOICES, default='prospecting')
    probability = models.IntegerField(choices=PROBABILITY_CHOICES, default=10)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    expected_close_date = models.DateField()
    actual_close_date = models.DateField(null=True, blank=True)
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_opportunities'
    )
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_opportunities'
    )
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Opportunity'
        verbose_name_plural = 'Opportunities'
    
    def __str__(self):
        return f"{self.name} - {self.contact.company or self.contact.get_full_name()}"
    
    def get_absolute_url(self):
        return reverse('crm:opportunity_detail', kwargs={'pk': self.pk})
    
    def get_weighted_amount(self):
        """Calculate weighted opportunity value"""
        return self.amount * (self.probability / 100)


class Activity(models.Model):
    """
    Activity Model - Track interactions and tasks
    """
    ACTIVITY_TYPE_CHOICES = [
        ('call', 'Phone Call'),
        ('meeting', 'Meeting'),
        ('email', 'Email'),
        ('task', 'Task'),
        ('note', 'Note'),
    ]
    
    STATUS_CHOICES = [
        ('planned', 'Planned'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]
    
    activity_type = models.CharField(max_length=20, choices=ACTIVITY_TYPE_CHOICES)
    subject = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='planned')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium')
    due_date = models.DateTimeField()
    completed_date = models.DateTimeField(null=True, blank=True)
    
    # Related objects
    lead = models.ForeignKey(
        Lead,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='activities'
    )
    contact = models.ForeignKey(
        Contact,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='activities'
    )
    opportunity = models.ForeignKey(
        Opportunity,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='activities'
    )
    
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_activities'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_activities'
    )
    
    class Meta:
        ordering = ['due_date']
        verbose_name = 'Activity'
        verbose_name_plural = 'Activities'
    
    def __str__(self):
        return f"{self.get_activity_type_display()} - {self.subject}"
    
    def get_absolute_url(self):
        return reverse('crm:activity_detail', kwargs={'pk': self.pk})
    
    def mark_completed(self):
        """Mark activity as completed"""
        self.status = 'completed'
        self.completed_date = timezone.now()
        self.save()
