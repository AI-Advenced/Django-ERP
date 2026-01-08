from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Q, Sum, F
from decimal import Decimal

from .models import Product, Category, Unit, Location, StockMovement, ProductLocation, Warehouse

# Warehouse Views
class WarehouseListView(ListView):
    model = Warehouse
    template_name = 'inventory/warehouse_list.html'
    context_object_name = 'warehouses'
    
# Product Views
class ProductListView(LoginRequiredMixin, ListView):
    """List all products"""
    model = Product
    template_name = 'inventory/product_list.html'
    context_object_name = 'products'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = Product.objects.select_related('category', 'unit', 'created_by')
        
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(code__icontains=search) |
                Q(name__icontains=search) |
                Q(barcode__icontains=search) |
                Q(sku__icontains=search)
            )
        
        category = self.request.GET.get('category')
        if category:
            queryset = queryset.filter(category_id=category)
        
        status = self.request.GET.get('status')
        if status == 'low_stock':
            queryset = queryset.filter(current_stock__lte=F('minimum_stock'))
        elif status == 'out_of_stock':
            queryset = queryset.filter(current_stock=0)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['total_products'] = Product.objects.count()
        context['low_stock_count'] = Product.objects.filter(
            current_stock__lte=F('minimum_stock')
        ).count()
        context['out_of_stock_count'] = Product.objects.filter(current_stock=0).count()
        return context


class ProductDetailView(LoginRequiredMixin, DetailView):
    """View product details"""
    model = Product
    template_name = 'inventory/product_detail.html'
    context_object_name = 'product'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['stock_movements'] = self.object.stock_movements.all()[:10]
        context['location_stock'] = self.object.location_stock.select_related('location')
        return context


class ProductCreateView(LoginRequiredMixin, CreateView):
    """Create new product"""
    model = Product
    template_name = 'inventory/product_form.html'
    fields = ['code', 'name', 'description', 'category', 'unit', 'cost_price', 'selling_price',
              'track_inventory', 'current_stock', 'minimum_stock', 'maximum_stock',
              'barcode', 'sku', 'manufacturer', 'brand', 'is_active']
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, 'Product created successfully!')
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    """Update product"""
    model = Product
    template_name = 'inventory/product_form.html'
    fields = ['code', 'name', 'description', 'category', 'unit', 'cost_price', 'selling_price',
              'track_inventory', 'current_stock', 'minimum_stock', 'maximum_stock',
              'barcode', 'sku', 'manufacturer', 'brand', 'is_active']
    
    def form_valid(self, form):
        messages.success(self.request, 'Product updated successfully!')
        return super().form_valid(form)


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    """Delete product"""
    model = Product
    template_name = 'inventory/product_confirm_delete.html'
    success_url = reverse_lazy('inventory:product_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Product deleted successfully!')
        return super().delete(request, *args, **kwargs)


# Category Views
class CategoryListView(LoginRequiredMixin, ListView):
    """List all categories"""
    model = Category
    template_name = 'inventory/category_list.html'
    context_object_name = 'categories'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_categories'] = Category.objects.count()
        return context


class CategoryCreateView(LoginRequiredMixin, CreateView):
    """Create new category"""
    model = Category
    template_name = 'inventory/category_form.html'
    fields = ['name', 'description', 'parent']
    success_url = reverse_lazy('inventory:category_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Category created successfully!')
        return super().form_valid(form)


# Location Views
class LocationListView(LoginRequiredMixin, ListView):
    """List all locations"""
    model = Location
    template_name = 'inventory/location_list.html'
    context_object_name = 'locations'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_locations'] = Location.objects.count()
        return context


class LocationDetailView(LoginRequiredMixin, DetailView):
    """View location details"""
    model = Location
    template_name = 'inventory/location_detail.html'
    context_object_name = 'location'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_stock'] = self.object.product_stock.select_related('product')
        return context


class LocationCreateView(LoginRequiredMixin, CreateView):
    """Create new location"""
    model = Location
    template_name = 'inventory/location_form.html'
    fields = ['name', 'code', 'description', 'address', 'is_default', 'is_active']
    
    def form_valid(self, form):
        messages.success(self.request, 'Location created successfully!')
        return super().form_valid(form)


# Stock Movement Views
class StockMovementListView(LoginRequiredMixin, ListView):
    """List all stock movements"""
    model = StockMovement
    template_name = 'inventory/movement_list.html'
    context_object_name = 'movements'
    paginate_by = 50
    
    def get_queryset(self):
        queryset = StockMovement.objects.select_related(
            'product', 'location_from', 'location_to', 'created_by'
        )
        
        movement_type = self.request.GET.get('type')
        if movement_type:
            queryset = queryset.filter(movement_type=movement_type)
        
        product_id = self.request.GET.get('product')
        if product_id:
            queryset = queryset.filter(product_id=product_id)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['movement_types'] = StockMovement.MOVEMENT_TYPE_CHOICES
        context['products'] = Product.objects.all()
        context['total_movements'] = StockMovement.objects.count()
        return context


class StockMovementDetailView(LoginRequiredMixin, DetailView):
    """View movement details"""
    model = StockMovement
    template_name = 'inventory/movement_detail.html'
    context_object_name = 'movement'


class StockMovementCreateView(LoginRequiredMixin, CreateView):
    """Create new stock movement"""
    model = StockMovement
    template_name = 'inventory/movement_form.html'
    fields = ['movement_type', 'product', 'quantity', 'location_from', 'location_to',
              'reference', 'notes', 'unit_cost']
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, 'Stock movement recorded successfully!')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('inventory:movement_list')


# Dashboard/Report Views
class InventoryDashboardView(LoginRequiredMixin, ListView):
    """Inventory dashboard with statistics"""
    model = Product
    template_name = 'inventory/dashboard.html'
    context_object_name = 'low_stock_products'
    
    def get_queryset(self):
        return Product.objects.filter(
            current_stock__lte=F('minimum_stock')
        ).order_by('current_stock')[:10]
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Statistics
        context['total_products'] = Product.objects.filter(is_active=True).count()
        context['total_categories'] = Category.objects.count()
        context['total_locations'] = Location.objects.filter(is_active=True).count()
        
        # Stock alerts
        context['low_stock_count'] = Product.objects.filter(
            current_stock__lte=F('minimum_stock'),
            track_inventory=True
        ).count()
        context['out_of_stock_count'] = Product.objects.filter(
            current_stock=0,
            track_inventory=True
        ).count()
        
        # Recent movements
        context['recent_movements'] = StockMovement.objects.select_related(
            'product', 'created_by'
        ).order_by('-created_at')[:10]
        
        # Total inventory value
        total_value = Product.objects.aggregate(
            total=Sum(F('current_stock') * F('cost_price'))
        )['total'] or Decimal('0.00')
        context['total_inventory_value'] = total_value
        
        return context
