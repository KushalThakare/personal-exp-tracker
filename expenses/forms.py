from django import forms
from django.utils import timezone
from .models import Expense


class ExpenseForm(forms.ModelForm):
    """
    Django ModelForm for creating and editing expenses.
    Handles input validation and styling attributes.
    """
    class Meta:
        model = Expense
        fields = ['title', 'amount', 'category', 'date', 'description']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. Grocery shopping, Metro card recharge',
                'required': True,
            }),
            'amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '0.00',
                'step': '0.01',
                'min': '0.01',
                'required': True,
            }),
            'category': forms.Select(attrs={
                'class': 'form-select',
                'required': True,
            }),
            'date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'required': True,
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Optional details, vendor name, or transaction notes...',
            }),
        }
        labels = {
            'title': 'Expense Title',
            'amount': 'Amount (₹)',
            'category': 'Category',
            'date': 'Expense Date',
            'description': 'Description (Optional)',
        }
        error_messages = {
            'title': {
                'required': 'Expense title cannot be empty.',
            },
            'amount': {
                'required': 'Please enter a valid expense amount.',
                'invalid': 'Please enter a valid numeric amount.',
            },
            'category': {
                'required': 'Please select an expense category.',
            },
            'date': {
                'required': 'Please specify the expense date.',
            },
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Default the date field to today if creating a new instance
        if not self.instance.pk and not self.initial.get('date'):
            self.initial['date'] = timezone.localdate()

    def clean_title(self):
        title = self.cleaned_data.get('title', '').strip()
        if not title:
            raise forms.ValidationError("Expense title cannot be empty.")
        return title

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if amount is not None and amount <= 0:
            raise forms.ValidationError("Expense amount must be greater than zero.")
        return amount
