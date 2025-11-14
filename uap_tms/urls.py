# TMS_/urls.py (or your_project_name/urls.py)
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView  # Add this import

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('buses.urls')),
    path('dashboard/', RedirectView.as_view(url='/'), name='dashboard'),  # Temporary
    path('accounts/', include('accounts.urls')),  # If you have accounts app
    path('payments/', include('payments.urls')),  # If you have payments app
path('logo', RedirectView.as_view(url='/static/images/uap-logo.png')),
    # ... your existing routes
    path('', include('your_main_app.urls')),
]