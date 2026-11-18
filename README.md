# Personal Expense Tracker (Django & SQLite)

A clean, modern, lightweight, and fully functional **Personal Expense Tracker** web application built with Python and Django.

> **Course Context**: Developed as a college case-study project for the **Meta Back-End Developer Professional Certificate** on Coursera. It demonstrates core back-end engineering concepts: Python programming, Django's Model-View-Template (MVT) architecture, SQLite database integration, ORM querying and aggregation, full CRUD operations, and HTTP request handling.

---

## 1. Project Overview

The Personal Expense Tracker helps individuals track their daily spending, monitor category-wise distribution, and analyze monthly totals. It features a responsive blue-and-white user interface with visual summaries, interactive charts, and standard server-side validation.

---

## 2. Technologies Used

- **Backend Framework**: Python 3.10+ / Django 5.x–6.x
- **Database**: SQLite3 (`db.sqlite3`)
- **Frontend**: Semantic HTML5, Custom Responsive CSS3, Vanilla JavaScript
- **Data Visualization**: Chart.js (CDN-hosted interactive doughnut chart)
- **Currency**: Indian Rupees (₹)
- **Architecture**: Model-View-Template (MVT)

---

## 3. Main Features

1. **Financial Dashboard (`/`)**:
   - Summary cards displaying **Total Expenses**, **Current Month Expenses**, and **Total Transactions**.
   - Recent transaction table showing the latest entries with category badges.
   - Category-wise spending breakdown with visual progress bars and an interactive doughnut chart.
   - Friendly empty-state prompt when no expenses exist.

2. **Add Expense (`/expenses/add/`)**:
   - Fields: Expense Title, Amount (₹), Category, Date, and optional Description.
   - Categories: `Food`, `Travel`, `Shopping`, `Education`, `Entertainment`, `Other`.
   - Comprehensive server-side validation rejecting non-positive amounts or empty titles.

3. **View & Filter Expenses (`/expenses/`)**:
   - Tabular history ordered newest first.
   - Category filter pills updating record counts and subtotal amounts dynamically.
   - Direct edit and delete action buttons for every record.

4. **Edit Expense (`/expenses/<id>/edit/`)**:
   - Form pre-populated with existing transaction values for fast editing.

5. **Delete Expense (`/expenses/<id>/delete/`)**:
   - Dedicated confirmation dialog preventing accidental deletions.
   - Executes safe HTTP POST requests with CSRF protection.

---

## 4. Folder Structure

```text
personal-exp-tracker/
│
├── manage.py                          # Django management CLI script
├── requirements.txt                   # Project Python dependencies
├── db.sqlite3                         # Local SQLite database file
├── README.md                          # Documentation & presentation guide
│
├── expense_tracker/                   # Main Django project configuration
│   ├── __init__.py
│   ├── asgi.py
│   ├── wsgi.py
│   ├── urls.py                        # Root URL routing configuration
│   └── settings.py                    # Project settings (apps, DB, templates, static)
│
├── expenses/                          # Core expense tracker app
│   ├── __init__.py
│   ├── admin.py                       # Django Admin registration
│   ├── apps.py                        # App configuration
│   ├── models.py                      # Expense database model definition
│   ├── forms.py                       # ExpenseForm validation logic
│   ├── views.py                       # Controller views (Dashboard, List, Add, Edit, Delete)
│   ├── urls.py                        # App-level URL routes
│   ├── tests.py                       # Automated unit test suite (9 tests passing)
│   ├── migrations/                    # Database migration history
│   │   ├── 0001_initial.py
│   │   └── __init__.py
│   └── management/                    # Custom Django management commands
│       └── commands/
│           ├── __init__.py
│           └── seed_expenses.py       # Seeds sample student expense records
│
├── static/                            # Static assets
│   ├── css/
│   │   └── style.css                  # Clean, modern, responsive CSS styling
│   └── js/
│       └── main.js                    # Flash message dismissals and helpers
│
└── templates/                         # HTML Templates (Django Template Language)
    ├── base.html                      # Base layout (Navbar, alerts, footer)
    └── expenses/
        ├── dashboard.html             # Summary cards, charts, and recent activity
        ├── expense_list.html          # Full table view with category filtering
        ├── expense_form.html          # Unified form for adding & editing expenses
        └── expense_confirm_delete.html# Deletion confirmation page
```

---

## 5. Step-by-Step Installation on Windows 11

### Prerequisites
Ensure **Python 3.10 or higher** is installed. Verify in PowerShell or Command Prompt:
```powershell
python --version
```

---

### Step 1: Open Terminal in Project Directory
```powershell
cd "E:\clg study\coursera\backend\expense_tracker\personal-exp-tracker"
```

---

### Step 2: (Optional) Set Up a Virtual Environment
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

---

### Step 3: Install Dependencies
```powershell
python -m pip install -r requirements.txt
```

---

### Step 4: Apply Database Migrations
```powershell
python manage.py makemigrations
python manage.py migrate
```

---

### Step 5: (Optional) Load Realistic Demo Data
```powershell
python manage.py seed_expenses
```

---

### Step 6: Start the Django Development Server
```powershell
python manage.py runserver
```

Open your browser and navigate to:
```text
http://127.0.0.1:8000/
```

---

## 6. Running the Automated Tests

To run the automated test suite covering all 12 review checkpoints (server health, CRUD persistence, filtering, monthly aggregations, and input validation):
```powershell
python manage.py test
```

Output:
```text
Ran 9 tests in 0.15s
OK
```

---

## 7. Deep Dive: Django Architecture & SQLite Integration

### 1. The Model (`expenses/models.py`)
The `Expense` model defines the database schema:
- `title`: Short descriptive name (e.g., "Grocery Shopping").
- `amount`: `DecimalField` storing exact currency values up to 2 decimal places.
- `category`: Choice field restricted to predefined categories.
- `date`: `DateField` storing transaction dates.
- `description`: Optional text field for additional notes.
- `created_at`: Auto timestamp for audit and secondary ordering.
- `ordering = ['-date', '-created_at']`: Ensures newest records always display first.

### 2. The Views (`expenses/views.py`)
Views contain the business logic:
- `dashboard`: Uses Django ORM's `aggregate(Sum('amount'))` to calculate total and current-month spending without loading all records into Python memory.
- `expense_list`: Applies category filters (`category=Food`) and computes filtered subtotals.
- `expense_create` / `expense_update`: Validates incoming data using `ExpenseForm` and saves to SQLite.
- `expense_delete`: Renders a GET confirmation prompt and permanently deletes the record on POST.

### 3. The Templates (`templates/`)
Templates use the **Django Template Language (DTL)**:
- Template inheritance via `base.html` ensures consistent navigation, alerts, and responsive meta tags.
- Dynamic data tags (`{{ exp.title }}`, `{{ total_expenses|floatformat:2 }}`) render server data securely.
- CSRF protection (`{% csrf_token %}`) is embedded in all POST forms.

### 4. SQLite Database Integration (`db.sqlite3`)
- SQLite runs serverless in a single local file (`db.sqlite3`), configured directly in `settings.py` via `django.db.backends.sqlite3`.
- Django migrations translate Python model definitions into SQLite SQL `CREATE TABLE` and `ALTER TABLE` statements automatically.

---

## 8. Short Explanation for a 2-Minute College Presentation

> **Speaker Script:**
>
> *"Good morning/afternoon everyone. Today, I am presenting my **Personal Expense Tracker**, a full-stack web application developed as part of the Meta Back-End Developer Professional Certificate on Coursera.*
>
> *The primary objective of this project is to demonstrate core back-end engineering principles using **Python**, **Django**, and **SQLite**.*
>
> *Here is how the system works:*
>
> 1. *First, the application follows Django's **Model-View-Template (MVT)** architecture. Our **Expense Model** represents our database schema with fields for title, amount, category, date, and description.*
> 2. *Second, for data persistence, we use **SQLite**. When an expense is recorded, Django's **ModelForm** validates that the title is not blank and the amount is strictly positive, safeguarding data integrity before committing to the database.*
> 3. *Third, on the **Dashboard**, our views leverage the **Django ORM** to execute aggregate database queries—specifically `Sum` and `Count`—to dynamically compute total lifetime spending, current month spending, and category-wise breakdowns, which are visualized using **Chart.js**.*
> 4. *Fourth, users have full **CRUD capabilities**: they can Create expenses, Read them in a filtered table, Update existing entries, and safely Delete them with CSRF-protected confirmation prompts.*
> 5. *Finally, the user interface is completely responsive, styled in a modern blue-and-white theme with clean typography and amounts displayed in Indian Rupees (₹).*
>
> *The project includes an automated test suite with 9 passing unit tests covering all CRUD operations, database queries, and input validation. Thank you!"*
