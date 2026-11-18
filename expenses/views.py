import json
from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum, Count
from django.utils import timezone
from django.contrib import messages
from .models import Expense
from .forms import ExpenseForm


def dashboard(request):
    """
    Dashboard view displaying:
    - Total expenses
    - Current month total expenses
    - Total transaction count
    - Recent transactions list
    - Category-wise breakdown with Chart.js data
    """
    today = timezone.localdate()
    current_year = today.year
    current_month = today.month

    # 1. Total expenses overall
    total_expenses = Expense.objects.aggregate(total=Sum('amount'))['total'] or Decimal('0.00')

    # 2. Total expenses for current month
    monthly_expenses = (
        Expense.objects.filter(date__year=current_year, date__month=current_month)
        .aggregate(total=Sum('amount'))['total'] or Decimal('0.00')
    )

    # 3. Total number of transactions
    total_transactions = Expense.objects.count()

    # 4. Recent expenses (latest 5)
    recent_expenses = Expense.objects.all()[:5]

    # 5. Category-wise expense breakdown
    category_data_qs = (
        Expense.objects.values('category')
        .annotate(total=Sum('amount'), count=Count('id'))
        .order_by('-total')
    )

    # Calculate percentage for each category
    category_summary = []
    for item in category_data_qs:
        pct = (float(item['total']) / float(total_expenses) * 100) if total_expenses > 0 else 0
        category_summary.append({
            'category': item['category'],
            'total': item['total'],
            'count': item['count'],
            'percentage': round(pct, 1),
        })

    # Prepare labels and values for Chart.js
    chart_labels = [item['category'] for item in category_summary]
    chart_values = [float(item['total']) for item in category_summary]

    context = {
        'total_expenses': total_expenses,
        'monthly_expenses': monthly_expenses,
        'total_transactions': total_transactions,
        'recent_expenses': recent_expenses,
        'category_summary': category_summary,
        'chart_labels_json': json.dumps(chart_labels),
        'chart_values_json': json.dumps(chart_values),
        'current_month_name': today.strftime('%B %Y'),
    }
    return render(request, 'expenses/dashboard.html', context)


def expense_list(request):
    """
    Expense list view with:
    - Category filter
    - Order by newest first
    - Action links to edit/delete
    - Summary of filtered expenses
    """
    selected_category = request.GET.get('category', '').strip()
    expenses = Expense.objects.all()

    if selected_category and selected_category != 'All':
        expenses = expenses.filter(category=selected_category)

    # Calculate summary metrics for the currently filtered view
    filtered_total = expenses.aggregate(total=Sum('amount'))['total'] or Decimal('0.00')
    filtered_count = expenses.count()

    # Available categories for filter dropdown
    categories = [choice[0] for choice in Expense.CATEGORY_CHOICES]

    context = {
        'expenses': expenses,
        'categories': categories,
        'selected_category': selected_category,
        'filtered_total': filtered_total,
        'filtered_count': filtered_count,
    }
    return render(request, 'expenses/expense_list.html', context)


def expense_create(request):
    """
    Create a new expense entry with validation.
    """
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save()
            messages.success(request, f"Expense '{expense.title}' of ₹{expense.amount} added successfully!")
            return redirect('expense_list')
    else:
        form = ExpenseForm()

    context = {
        'form': form,
        'page_title': 'Add New Expense',
        'is_edit': False,
    }
    return render(request, 'expenses/expense_form.html', context)


def expense_update(request, pk):
    """
    Update an existing expense entry.
    """
    expense = get_object_or_404(Expense, pk=pk)

    if request.method == 'POST':
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            updated_expense = form.save()
            messages.success(request, f"Expense '{updated_expense.title}' updated successfully!")
            return redirect('expense_list')
    else:
        form = ExpenseForm(instance=expense)

    context = {
        'form': form,
        'expense': expense,
        'page_title': 'Edit Expense',
        'is_edit': True,
    }
    return render(request, 'expenses/expense_form.html', context)


def expense_delete(request, pk):
    """
    Delete an expense after user confirmation.
    """
    expense = get_object_or_404(Expense, pk=pk)

    if request.method == 'POST':
        title = expense.title
        amount = expense.amount
        expense.delete()
        messages.success(request, f"Expense '{title}' (₹{amount}) was deleted.")
        return redirect('expense_list')

    context = {
        'expense': expense,
    }
    return render(request, 'expenses/expense_confirm_delete.html', context)
