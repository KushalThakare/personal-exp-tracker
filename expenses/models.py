from django.db import models


class Expense(models.Model):
    """
    Model representing an individual expense entry.
    Demonstrates Django ORM fields, choices, and default ordering.
    """
    CATEGORY_CHOICES = [
        ('Food', 'Food'),
        ('Travel', 'Travel'),
        ('Shopping', 'Shopping'),
        ('Education', 'Education'),
        ('Entertainment', 'Entertainment'),
        ('Other', 'Other'),
    ]

    title = models.CharField(max_length=150, help_text="Expense title or brief name")
    amount = models.DecimalField(max_digits=10, decimal_places=2, help_text="Amount in ₹ (Rupees)")
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='Food')
    date = models.DateField(help_text="Date of expense")
    description = models.TextField(blank=True, null=True, help_text="Optional description/notes")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Record creation timestamp")

    class Meta:
        # Show newest expenses first by date, then by creation timestamp
        ordering = ['-date', '-created_at']
        verbose_name = 'Expense'
        verbose_name_plural = 'Expenses'

    def __str__(self):
        return f"{self.title} (₹{self.amount})"
