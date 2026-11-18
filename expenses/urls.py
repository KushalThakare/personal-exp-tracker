from django.urls import path
from . import views

urlpatterns = [
    # Dashboard page (home)
    path('', views.dashboard, name='dashboard'),

    # Expense List & Filter page
    path('expenses/', views.expense_list, name='expense_list'),

    # Create new expense
    path('expenses/add/', views.expense_create, name='expense_create'),

    # Edit existing expense
    path('expenses/<int:pk>/edit/', views.expense_update, name='expense_update'),

    # Delete existing expense
    path('expenses/<int:pk>/delete/', views.expense_delete, name='expense_delete'),
]
