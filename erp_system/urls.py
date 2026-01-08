from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('base.urls')),
    path('users/', include('users.urls')),
    path('crm/', include('crm.urls')),
    path('inventory/', include('inventory.urls')),
    path('financial/', include('financial.urls')),
    path('fiscal/', include('fiscal.urls')),
    path('sales/', include('sales.urls')),
    path('purchasing/', include('purchasing.urls')),
    path('hr/', include('hr.urls')),
    path('logistics/', include('logistics.urls')),
    path('projects/', include('projects.urls')),
    path('quality/', include('quality.urls')),
    path('maintenance/', include('maintenance.urls')),
    path('bi/', include('bi_reporting.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
