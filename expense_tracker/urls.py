"""
URL configuration for expense_tracker project.
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # Delegate application routes to expenses app
    path('', include('expenses.urls')),
]
