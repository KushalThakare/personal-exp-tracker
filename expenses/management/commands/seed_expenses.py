from decimal import Decimal
from datetime import date, timedelta
from django.core.management.base import BaseCommand
from expenses.models import Expense


class Command(BaseCommand):
    help = 'Populate the database with sample expense data for demonstration.'

    def handle(self, *args, **options):
        today = date.today()

        sample_data = [
            {
                'title': 'College Canteen Lunch',
                'amount': Decimal('160.00'),
                'category': 'Food',
                'date': today,
                'description': 'Lunch with project teammates at college food court.',
            },
            {
                'title': 'Metro Smart Card Recharge',
                'amount': Decimal('500.00'),
                'category': 'Travel',
                'date': today - timedelta(days=1),
                'description': 'Monthly commuting balance recharge.',
            },
            {
                'title': 'Python & Django Course Book',
                'amount': Decimal('650.00'),
                'category': 'Education',
                'date': today - timedelta(days=2),
                'description': 'Reference book for Web Development course.',
            },
            {
                'title': 'Movie Ticket & Popcorn',
                'amount': Decimal('420.00'),
                'category': 'Entertainment',
                'date': today - timedelta(days=4),
                'description': 'Weekend movie with friends at PVR.',
            },
            {
                'title': 'Notebooks & Stationery',
                'amount': Decimal('280.00'),
                'category': 'Shopping',
                'date': today - timedelta(days=6),
                'description': 'College spiral notebooks, pens, and highlighters.',
            },
            {
                'title': 'Mobile Recharge (3 Months)',
                'amount': Decimal('719.00'),
                'category': 'Other',
                'date': today - timedelta(days=8),
                'description': 'Quarterly 5G data plan recharge.',
            },
            {
                'title': 'Evening Snacks & Tea',
                'amount': Decimal('85.00'),
                'category': 'Food',
                'date': today - timedelta(days=10),
                'description': 'Tea and samosas after lab sessions.',
            },
            {
                'title': 'Auto Rickshaw Fare',
                'amount': Decimal('120.00'),
                'category': 'Travel',
                'date': today - timedelta(days=12),
                'description': 'Ride to railway station.',
            },
        ]

        created_count = 0
        for item in sample_data:
            _, created = Expense.objects.get_or_create(
                title=item['title'],
                date=item['date'],
                defaults=item
            )
            if created:
                created_count += 1

        self.stdout.write(
            self.style.SUCCESS(f"Successfully loaded {created_count} sample expense record(s) into database.")
        )
