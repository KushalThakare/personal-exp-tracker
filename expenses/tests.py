from decimal import Decimal
from datetime import date, timedelta
from django.test import TestCase, Client
from django.urls import reverse
from .models import Expense


class ExpenseTrackerTests(TestCase):
    """
    Comprehensive test suite verifying:
    1. Server / Views load properly
    2. Adding expenses and SQLite database persistence
    3. Editing existing expenses
    4. Deleting expenses with confirmation
    5. Category filtering
    6. Total and Monthly expense calculations
    7. Input validation and error handling
    8. Navigation routes and responsive metadata
    """

    def setUp(self):
        self.client = Client()
        self.today = date.today()

        # Item 1: Food expense this month
        self.exp1 = Expense.objects.create(
            title="College Canteen Lunch",
            amount=Decimal("150.00"),
            category="Food",
            date=self.today,
            description="Lunch with project team"
        )
        # Item 2: Travel expense this month
        self.exp2 = Expense.objects.create(
            title="Monthly Metro Pass",
            amount=Decimal("800.00"),
            category="Travel",
            date=self.today,
            description="Metro Smart Card recharge"
        )
        # Item 3: Education expense this month
        self.exp3 = Expense.objects.create(
            title="Data Structures Textbook",
            amount=Decimal("450.00"),
            category="Education",
            date=self.today,
            description="Reference book for semester exams"
        )

    def test_dashboard_view_with_data(self):
        """1 & 2: Dashboard loads correctly with summary cards and recent items."""
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Expense Dashboard")
        self.assertContains(response, "College Canteen Lunch")
        self.assertEqual(response.context['total_transactions'], 3)
        self.assertEqual(response.context['total_expenses'], Decimal("1400.00"))
        self.assertEqual(response.context['monthly_expenses'], Decimal("1400.00"))

    def test_empty_dashboard_renders_friendly_message(self):
        """Dashboard renders gracefully with friendly message when 0 expenses exist."""
        Expense.objects.all().delete()
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['total_transactions'], 0)
        self.assertEqual(response.context['total_expenses'], Decimal("0.00"))
        self.assertEqual(response.context['monthly_expenses'], Decimal("0.00"))
        self.assertContains(response, "No expenses recorded yet")

    def test_expense_list_view_and_filtering(self):
        """7: Expense list displays items and filters by category."""
        # Unfiltered list
        response = self.client.get(reverse('expense_list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['expenses']), 3)

        # Filter by category Food
        response_food = self.client.get(reverse('expense_list'), {'category': 'Food'})
        self.assertEqual(response_food.status_code, 200)
        self.assertEqual(len(response_food.context['expenses']), 1)
        self.assertEqual(response_food.context['filtered_total'], Decimal("150.00"))

        # Filter by category Travel
        response_travel = self.client.get(reverse('expense_list'), {'category': 'Travel'})
        self.assertEqual(response_travel.status_code, 200)
        self.assertEqual(len(response_travel.context['expenses']), 1)
        self.assertEqual(response_travel.context['filtered_total'], Decimal("800.00"))

        # Filter by category with no expenses
        response_shopping = self.client.get(reverse('expense_list'), {'category': 'Shopping'})
        self.assertEqual(response_shopping.status_code, 200)
        self.assertEqual(len(response_shopping.context['expenses']), 0)
        self.assertContains(response_shopping, "No expenses found")

    def test_create_expense_persists_in_sqlite(self):
        """3 & 4: Users can add new expenses and save to SQLite."""
        payload = {
            'title': 'Cinema Ticket',
            'amount': '320.00',
            'category': 'Entertainment',
            'date': self.today.isoformat(),
            'description': 'Weekend movie ticket',
        }
        response = self.client.post(reverse('expense_create'), data=payload, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Expense.objects.filter(title='Cinema Ticket').exists())
        new_exp = Expense.objects.get(title='Cinema Ticket')
        self.assertEqual(new_exp.amount, Decimal('320.00'))
        self.assertEqual(new_exp.category, 'Entertainment')
        self.assertEqual(new_exp.description, 'Weekend movie ticket')

    def test_update_expense_mutates_database(self):
        """5: Users can edit existing expenses."""
        payload = {
            'title': 'College Canteen Deluxe Lunch',
            'amount': '220.00',
            'category': 'Food',
            'date': self.today.isoformat(),
            'description': 'Updated lunch price',
        }
        response = self.client.post(reverse('expense_update', args=[self.exp1.pk]), data=payload, follow=True)
        self.assertEqual(response.status_code, 200)
        self.exp1.refresh_from_db()
        self.assertEqual(self.exp1.title, 'College Canteen Deluxe Lunch')
        self.assertEqual(self.exp1.amount, Decimal('220.00'))

    def test_delete_expense_removes_from_database(self):
        """6: Users can delete expenses after confirmation."""
        exp_id = self.exp3.pk
        # GET confirmation page
        get_confirm = self.client.get(reverse('expense_delete', args=[exp_id]))
        self.assertEqual(get_confirm.status_code, 200)
        self.assertContains(get_confirm, "Confirm Deletion")

        # POST deletion
        response = self.client.post(reverse('expense_delete', args=[exp_id]), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Expense.objects.filter(pk=exp_id).exists())

    def test_total_and_monthly_expense_calculations(self):
        """8 & 9: Verify total and current-month calculations distinguish past months."""
        # Add an expense from an earlier month or past year (e.g. 60 days ago)
        past_date = self.today - timedelta(days=60)
        Expense.objects.create(
            title="Past Exam Fee",
            amount=Decimal("500.00"),
            category="Education",
            date=past_date
        )

        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        # Total should include the past expense (1400 + 500 = 1900)
        self.assertEqual(response.context['total_expenses'], Decimal("1900.00"))
        # Monthly total should only include current month's expenses (1400.00)
        self.assertEqual(response.context['monthly_expenses'], Decimal("1400.00"))
        self.assertEqual(response.context['total_transactions'], 4)

    def test_invalid_inputs_handling(self):
        """10: Application handles invalid inputs properly."""
        # Negative amount
        res_neg = self.client.post(reverse('expense_create'), data={
            'title': 'Negative amount',
            'amount': '-50.00',
            'category': 'Food',
            'date': self.today.isoformat(),
        })
        self.assertEqual(res_neg.status_code, 200)
        self.assertFormError(res_neg.context['form'], 'amount', 'Expense amount must be greater than zero.')

        # Zero amount
        res_zero = self.client.post(reverse('expense_create'), data={
            'title': 'Zero amount',
            'amount': '0.00',
            'category': 'Food',
            'date': self.today.isoformat(),
        })
        self.assertEqual(res_zero.status_code, 200)
        self.assertFormError(res_zero.context['form'], 'amount', 'Expense amount must be greater than zero.')

        # Empty title
        res_empty = self.client.post(reverse('expense_create'), data={
            'title': '   ',
            'amount': '100.00',
            'category': 'Food',
            'date': self.today.isoformat(),
        })
        self.assertEqual(res_empty.status_code, 200)
        self.assertFormError(res_empty.context['form'], 'title', 'Expense title cannot be empty.')

        # Non-existent ID should return 404
        res_404 = self.client.get(reverse('expense_update', args=[99999]))
        self.assertEqual(res_404.status_code, 404)

    def test_all_navigation_routes_and_responsive_markup(self):
        """11 & 12: All navigation links resolve with HTTP 200 and mobile viewport is configured."""
        routes = [
            reverse('dashboard'),
            reverse('expense_list'),
            reverse('expense_create'),
            reverse('expense_update', args=[self.exp1.pk]),
            reverse('expense_delete', args=[self.exp1.pk]),
        ]
        for route in routes:
            resp = self.client.get(route)
            self.assertEqual(resp.status_code, 200)
            # Verify responsive viewport meta tag is rendered
            self.assertContains(resp, 'name="viewport"')
            self.assertContains(resp, 'width=device-width')
