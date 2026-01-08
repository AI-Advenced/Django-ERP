# 🏢 Enterprise Resource Planning (Django-ERP) System

<div align="center">

![ERP System](https://img.shields.io/badge/ERP-System-blue.svg)
![Django](https://img.shields.io/badge/Django-4.2+-green.svg)
![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-purple.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Status](https://img.shields.io/badge/Status-Production_Ready-brightgreen.svg)

**A comprehensive, modern, and scalable ERP solution built with Django**

[Features](#-key-features) • [Installation](#-installation) • [Documentation](#-documentation) • [Modules](#-modules) • [Demo](#-demo) • [Contributing](#-contributing)

</div>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Key Features](#-key-features)
- [System Architecture](#-system-architecture)
- [Modules](#-modules)
- [Technology Stack](#-technology-stack)
- [Installation](#-installation)
- [Quick Start](#-quick-start)
- [Configuration](#-configuration)
- [Usage](#-usage)
- [API Documentation](#-api-documentation)
- [Testing](#-testing)
- [Deployment](#-deployment)
- [Screenshots](#-screenshots)
- [Contributing](#-contributing)
- [Support](#-support)
- [License](#-license)
- [Roadmap](#-roadmap)
- [Credits](#-credits)

---

## 🌟 Overview

**EERRPP (Enterprise Resource Planning Platform)** is a modern, full-featured ERP system designed to streamline business operations and improve organizational efficiency. Built with Django and modern web technologies, it provides a robust, scalable, and user-friendly solution for managing all aspects of your business.

### Why Choose EERRPP?

- 🚀 **Modern Architecture** - Built with Django 4.2+ and latest web technologies
- 🎨 **Beautiful UI/UX** - Responsive Bootstrap 5 interface with intuitive design
- 🔐 **Enterprise Security** - Industry-standard security practices and authentication
- 📊 **Real-time Analytics** - Comprehensive dashboards and reporting
- 🔌 **Modular Design** - Easy to extend and customize
- 🌍 **Multi-language Ready** - Internationalization support
- 📱 **Mobile Responsive** - Works seamlessly on all devices
- ⚡ **High Performance** - Optimized for speed and scalability

---

## ✨ Key Features

### 🎯 Core Capabilities

- **Multi-Module Architecture** - Integrated modules for complete business management
- **Role-Based Access Control** - Granular permissions and user management
- **Real-time Dashboard** - Live metrics and KPIs
- **Advanced Reporting** - Customizable reports and analytics
- **Workflow Automation** - Automated business processes
- **Document Management** - Centralized document storage and versioning
- **Audit Trail** - Complete activity logging and tracking
- **RESTful API** - Comprehensive API for integrations

### 🔒 Security Features

- ✅ CSRF Protection
- ✅ SQL Injection Prevention
- ✅ XSS Protection
- ✅ Secure Authentication & Authorization
- ✅ Password Encryption
- ✅ Session Management
- ✅ API Rate Limiting
- ✅ Security Headers

### 📈 Business Intelligence

- Interactive Dashboards
- Custom Report Builder
- Data Export (PDF, Excel, CSV)
- Scheduled Reports
- Visual Analytics
- Trend Analysis
- Forecasting Tools

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      Presentation Layer                      │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │   Web    │  │  Mobile  │  │   API    │  │  Admin   │   │
│  │Interface │  │   View   │  │Endpoints │  │  Panel   │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
└─────────────────────────────────────────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                      Application Layer                       │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │   CRM    │  │  Sales   │  │Financial │  │Inventory │   │
│  │  Module  │  │  Module  │  │  Module  │  │  Module  │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │  Fiscal  │  │   HR     │  │   Users  │  │   Base   │   │
│  │  Module  │  │  Module  │  │  Module  │  │  Module  │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
└─────────────────────────────────────────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                       Business Layer                         │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │ Business │  │Validation│  │Workflow  │  │  Signal  │   │
│  │  Logic   │  │  Rules   │  │  Engine  │  │ Handlers │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
└─────────────────────────────────────────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                        Data Layer                            │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │   ORM    │  │  Cache   │  │  File    │  │  Queue   │   │
│  │(Django)  │  │  Redis   │  │ Storage  │  │  Celery  │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
│                      PostgreSQL / MySQL                      │
└─────────────────────────────────────────────────────────────┘
```

---

## 📦 Modules

### 1. 🏠 **Base Module**
> Core system functionality and dashboard

**Features:**
- System dashboard with KPIs
- User notifications
- Activity feed
- System settings
- Quick actions

**Key Models:** Configuration, Notification, Activity

---

### 2. 👥 **CRM (Customer Relationship Management)**
> Manage leads, contacts, and customer relationships

**Features:**
- Lead management with status workflow
- Contact database with full profiles
- Opportunity tracking
- Activity logging (calls, meetings, emails)
- Sales pipeline visualization
- Lead conversion to customers
- Follow-up reminders

**Key Models:** Lead, Contact, Opportunity, Activity

**Workflows:**
```
Lead → Qualified → Opportunity → Converted → Customer
```

---

### 3. 💰 **Sales Module**
> Complete sales order and quotation management

**Features:**
- Customer management (Individual & Business)
- Sales order creation with line items
- Quotation generation
- One-click quotation to order conversion
- Order status workflow (Draft → Paid)
- Pricing with tax and discount support
- Shipping cost management
- Payment tracking
- Sales analytics dashboard

**Key Models:** Customer, SalesOrder, SalesOrderItem, Quotation, QuotationItem

**Workflows:**
```
Quotation → Accepted → Sales Order → Processing → Delivered → Invoiced → Paid
```

**Statistics:**
- 5 Models with 74 fields
- 16 Views (CRUD + Dashboard)
- 21 URL patterns
- 7 Admin interfaces

---

### 4. 💵 **Financial Module**
> Comprehensive financial management and accounting

**Features:**
- Chart of accounts
- Journal entries
- Invoicing system
- Bill management
- Payment processing
- Expense tracking
- Budget management
- Customer account management
- Financial reporting
- Reconciliation

**Key Models:** Account, Invoice, Bill, Payment, Expense, JournalEntry, Budget, Customer

**Workflows:**
```
Invoice → Sent → Paid
Bill → Received → Paid
```

---

### 5. 📊 **Fiscal Module**
> Tax management and compliance

**Features:**
- Tax rate management
- Fiscal year configuration
- Tax report generation
- Invoice tracking
- Payment recording
- Compliance reporting
- Multi-tax support (VAT, Sales Tax, etc.)

**Key Models:** TaxRate, FiscalYear, Invoice, Payment, TaxReport

---

### 6. 📦 **Inventory Module**
> Stock and warehouse management

**Features:**
- Product catalog
- Category management
- Stock tracking
- Warehouse management
- Stock movements
- Low stock alerts
- Barcode support
- Serial number tracking
- Inventory valuation

**Key Models:** Product, Category, StockMovement, Warehouse

---

### 7. 👤 **Users Module**
> User management and authentication

**Features:**
- User registration and authentication
- Role-based access control
- Permission management
- User profiles
- Password management
- Session management
- Activity tracking

**Key Models:** User, Role, Permission, Profile

---

## 🛠️ Technology Stack

### Backend
- **Framework:** Django 4.2+
- **Language:** Python 3.8+
- **Database:** PostgreSQL / MySQL / SQLite
- **ORM:** Django ORM
- **Authentication:** Django Auth + JWT
- **API:** Django REST Framework
- **Task Queue:** Celery (optional)
- **Cache:** Redis (optional)

### Frontend
- **Framework:** Bootstrap 5.3
- **Icons:** Font Awesome 6.4
- **Charts:** Chart.js
- **JavaScript:** Vanilla JS / jQuery
- **CSS:** Custom CSS + Bootstrap

### Development Tools
- **Version Control:** Git
- **Package Manager:** pip / pipenv
- **Testing:** pytest / Django TestCase
- **Code Quality:** flake8, black, pylint
- **Documentation:** Sphinx

### Deployment
- **Web Server:** Nginx / Apache
- **WSGI:** Gunicorn / uWSGI
- **Containerization:** Docker (optional)
- **CI/CD:** GitHub Actions / GitLab CI

---

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- virtualenv (recommended)
- PostgreSQL / MySQL (optional, SQLite for development)
- Git

### Step-by-Step Installation

#### 1. Clone the Repository

```bash
git clone https://github.com/AI-Advenced/Django-ERP.git
cd Django-ERP
```

#### 2. Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

#### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

#### 4. Configure Database

**Option A: Using SQLite (Development)**
```python
# settings.py - Default configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

**Option B: Using PostgreSQL (Production)**
```python
# settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'eerrpp_db',
        'USER': 'your_username',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

#### 5. Environment Variables

Create `.env` file in project root:

```env
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DB_ENGINE=django.db.backends.postgresql
DB_NAME=eerrpp_db
DB_USER=your_username
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432

# Email Configuration
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-email-password

# Static/Media Files
STATIC_URL=/static/
MEDIA_URL=/media/

# Security (Production)
SECURE_SSL_REDIRECT=False
SESSION_COOKIE_SECURE=False
CSRF_COOKIE_SECURE=False
```

#### 6. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

#### 7. Create Superuser

```bash
python manage.py createsuperuser
```

Follow the prompts to create an admin account.

#### 8. Collect Static Files

```bash
python manage.py collectstatic --noinput
```

#### 9. Run Development Server

```bash
python manage.py runserver
```

Visit: **http://localhost:8000**

---

## ⚡ Quick Start

### 1. Access the Application

```
Main Application: http://localhost:8000
Admin Panel: http://localhost:8000/admin
```

### 2. Initial Setup

1. **Login** with your superuser credentials
2. **Configure System Settings** in the admin panel
3. **Create User Roles** and assign permissions
4. **Add Initial Data**:
   - Chart of accounts
   - Product categories
   - Tax rates
   - Customer types

### 3. Module Access

```
CRM:       http://localhost:8000/crm/
Sales:     http://localhost:8000/sales/
Financial: http://localhost:8000/financial/
Fiscal:    http://localhost:8000/fiscal/
Inventory: http://localhost:8000/inventory/
```

### 4. Create Sample Data

```bash
# Option 1: Using Django shell
python manage.py shell

from sales.models import Customer
Customer.objects.create(
    name="Acme Corporation",
    email="contact@acme.com",
    customer_type="business",
    status="active"
)
```

```bash
# Option 2: Using fixtures (if available)
python manage.py loaddata sample_data.json
```

---

## ⚙️ Configuration

### Settings Overview

```python
# erp_system/settings.py

# Core Settings
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # ERP Modules
    'base',
    'users',
    'crm',
    'sales',
    'financial',
    'fiscal',
    'inventory',
]

# Security Settings
SECRET_KEY = env('SECRET_KEY')
DEBUG = env.bool('DEBUG', default=False)
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS')

# Database Configuration
DATABASES = {
    'default': {
        'ENGINE': env('DB_ENGINE'),
        'NAME': env('DB_NAME'),
        'USER': env('DB_USER'),
        'PASSWORD': env('DB_PASSWORD'),
        'HOST': env('DB_HOST'),
        'PORT': env('DB_PORT'),
    }
}

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

### URL Configuration

```python
# erp_system/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('base.urls')),
    path('users/', include('users.urls')),
    path('crm/', include('crm.urls')),
    path('sales/', include('sales.urls')),
    path('financial/', include('financial.urls')),
    path('fiscal/', include('fiscal.urls')),
    path('inventory/', include('inventory.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
```

---

## 📖 Usage

### Sales Module Example

#### Creating a Customer

```python
from sales.models import Customer

customer = Customer.objects.create(
    name="John Doe",
    email="john@example.com",
    phone="+1234567890",
    customer_type="individual",
    status="active",
    address="123 Main St",
    city="New York",
    country="USA"
)
```

#### Creating a Sales Order

```python
from sales.models import SalesOrder, SalesOrderItem
from decimal import Decimal

# Create order
order = SalesOrder.objects.create(
    customer=customer,
    order_number="SO-001",
    status="draft",
    tax_rate=Decimal("10.00")
)

# Add line items
SalesOrderItem.objects.create(
    sales_order=order,
    description="Product A",
    quantity=Decimal("5"),
    unit_price=Decimal("100.00")
)

# Calculate totals (automatic via model methods)
order.calculate_totals()
order.save()
```

#### Converting Quotation to Order

```python
from sales.models import Quotation

quotation = Quotation.objects.get(id=1)
quotation.status = 'accepted'
quotation.save()

# Convert to order
sales_order = quotation.convert_to_order()
```

### Financial Module Example

#### Creating an Invoice

```python
from financial.models import Invoice, Customer

invoice = Invoice.objects.create(
    customer=customer,
    invoice_number="INV-001",
    invoice_date="2026-01-08",
    due_date="2026-02-08",
    status="sent",
    subtotal=Decimal("500.00"),
    tax_rate=Decimal("10.00")
)

invoice.calculate_total()
invoice.save()
```

---

## 🔌 API Documentation

### Authentication

All API endpoints require authentication using JWT tokens.

```bash
# Get access token
POST /api/auth/login/
{
    "username": "user",
    "password": "password"
}

# Use token in requests
Authorization: Bearer <access_token>
```

### Endpoints

#### Sales API

```bash
# List customers
GET /api/sales/customers/

# Create customer
POST /api/sales/customers/
{
    "name": "Company Name",
    "email": "contact@company.com",
    "customer_type": "business"
}

# Get customer detail
GET /api/sales/customers/{id}/

# Update customer
PUT /api/sales/customers/{id}/

# Delete customer
DELETE /api/sales/customers/{id}/
```

#### Orders API

```bash
# List orders
GET /api/sales/orders/?status=confirmed

# Create order
POST /api/sales/orders/

# Get order detail
GET /api/sales/orders/{id}/
```

---

## 🧪 Testing

### Running Tests

```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test sales

# Run with coverage
coverage run --source='.' manage.py test
coverage report
coverage html
```

### Writing Tests

```python
# sales/tests.py

from django.test import TestCase
from sales.models import Customer

class CustomerModelTest(TestCase):
    def setUp(self):
        self.customer = Customer.objects.create(
            name="Test Customer",
            email="test@example.com",
            customer_type="individual",
            status="active"
        )
    
    def test_customer_creation(self):
        self.assertEqual(self.customer.name, "Test Customer")
        self.assertEqual(self.customer.status, "active")
    
    def test_customer_str(self):
        self.assertEqual(str(self.customer), "Test Customer")
```

---

## 🚢 Deployment

### Production Checklist

- [ ] Set `DEBUG = False`
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Use strong `SECRET_KEY`
- [ ] Set up PostgreSQL/MySQL
- [ ] Configure static file serving
- [ ] Set up media file storage
- [ ] Configure email backend
- [ ] Enable HTTPS
- [ ] Set secure cookies
- [ ] Configure logging
- [ ] Set up backups
- [ ] Configure monitoring

### Using Gunicorn

```bash
# Install Gunicorn
pip install gunicorn

# Run with Gunicorn
gunicorn erp_system.wsgi:application --bind 0.0.0.0:8000 --workers 4
```

### Using Docker

```dockerfile
# Dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

RUN python manage.py collectstatic --noinput

CMD ["gunicorn", "erp_system.wsgi:application", "--bind", "0.0.0.0:8000"]
```

```yaml
# docker-compose.yml
version: '3.8'

services:
  db:
    image: postgres:14
    environment:
      POSTGRES_DB: eerrpp_db
      POSTGRES_USER: eerrpp_user
      POSTGRES_PASSWORD: secure_password
    volumes:
      - postgres_data:/var/lib/postgresql/data

  web:
    build: .
    command: gunicorn erp_system.wsgi:application --bind 0.0.0.0:8000
    volumes:
      - .:/app
      - static_volume:/app/staticfiles
      - media_volume:/app/media
    ports:
      - "8000:8000"
    depends_on:
      - db

volumes:
  postgres_data:
  static_volume:
  media_volume:
```

---

## 📸 Screenshots

### Dashboard
<img width="1514" height="662" alt="image" src="https://github.com/user-attachments/assets/a5d7f009-509f-4f61-af71-5f761d936766" />


### Sales Module
<img width="1518" height="660" alt="image" src="https://github.com/user-attachments/assets/ae1a1b6b-2761-4aad-8bde-e4cd50893834" />


### Financial Module
<img width="1517" height="662" alt="image" src="https://github.com/user-attachments/assets/16468f95-03fe-4be5-ac77-437793bf619d" />


### CRM Module
<img width="1516" height="659" alt="image" src="https://github.com/user-attachments/assets/5acfcfbb-218f-4a97-8ed5-ec15513a0fce" />


---

## 🤝 Contributing

We welcome contributions from the community! Here's how you can help:

### How to Contribute

1. **Fork the Repository**
   ```bash
   git clone https://github.com/AI-Advenced/EERRPP.git
   cd EERRPP
   ```

2. **Create a Feature Branch**
   ```bash
   git checkout -b feature/AmazingFeature
   ```

3. **Make Your Changes**
   - Write clean, documented code
   - Follow PEP 8 style guide
   - Add tests for new features
   - Update documentation

4. **Commit Your Changes**
   ```bash
   git commit -m "Add: Amazing new feature"
   ```

5. **Push to Your Branch**
   ```bash
   git push origin feature/AmazingFeature
   ```

6. **Open a Pull Request**
   - Provide a clear description
   - Reference any related issues
   - Ensure all tests pass

### Contribution Guidelines

- **Code Style**: Follow PEP 8
- **Testing**: Write tests for new features
- **Documentation**: Update docs for changes
- **Commits**: Use clear, descriptive commit messages
- **Pull Requests**: One feature per PR

### Code of Conduct

Please read our [Code of Conduct](CODE_OF_CONDUCT.md) before contributing.

---

## 📞 Support

### Getting Help

- **Documentation**: Check our comprehensive docs
- **GitHub Issues**: [Report bugs or request features](https://github.com/AI-Advenced/Django-ERP/issues)
- **Discussions**: [Join community discussions](https://github.com/AI-Advenced/Django-ERP/discussions)
- **Email**: support@eerrpp.com

### Frequently Asked Questions

**Q: What are the system requirements?**
A: Python 3.8+, 2GB RAM minimum, PostgreSQL/MySQL for production

**Q: Is it free to use?**
A: Yes, it's open-source under MIT license

**Q: Can I customize the modules?**
A: Absolutely! The system is designed to be extensible

**Q: Is there commercial support available?**
A: Contact us for enterprise support options

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2026 EERRPP Team

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 🗓️ Roadmap

### Version 2.0 (Q2 2026)
- [ ] RESTful API with full documentation
- [ ] Mobile application (iOS/Android)
- [ ] Advanced analytics and BI tools
- [ ] Automated workflow builder
- [ ] Integration marketplace
- [ ] Multi-currency support
- [ ] Multi-language interface

### Version 2.5 (Q4 2026)
- [ ] AI-powered insights
- [ ] Machine learning forecasting
- [ ] Advanced inventory optimization
- [ ] E-commerce integration
- [ ] Payment gateway integration
- [ ] Automated invoicing
- [ ] Document generation

### Version 3.0 (Q2 2027)
- [ ] Microservices architecture
- [ ] Real-time collaboration
- [ ] Advanced security features
- [ ] Cloud-native deployment
- [ ] GraphQL API
- [ ] Progressive Web App
- [ ] Blockchain integration

---

## 👏 Credits

### Development Team

- **Project Lead**: AI Assistant
- **Backend Development**: Django Team
- **Frontend Development**: UI/UX Team
- **Database Design**: Data Architecture Team
- **Testing**: QA Team

### Technologies Used

- [Django](https://www.djangoproject.com/) - Web framework
- [Bootstrap](https://getbootstrap.com/) - CSS framework
- [Font Awesome](https://fontawesome.com/) - Icons
- [Chart.js](https://www.chartjs.org/) - Charts
- [PostgreSQL](https://www.postgresql.org/) - Database

### Special Thanks

- Django Software Foundation
- Bootstrap team
- Open-source community
- All contributors

---

## 📊 Project Stats

![GitHub stars](https://img.shields.io/github/stars/AI-Advenced/Django-ERP?style=social)
![GitHub forks](https://img.shields.io/github/forks/AI-Advenced/Django-ERP?style=social)
![GitHub watchers](https://img.shields.io/github/watchers/AI-Advenced/Django-ERP?style=social)

![GitHub last commit](https://img.shields.io/github/last-commit/AI-Advenced/Django-ERP)
![GitHub issues](https://img.shields.io/github/issues/AI-Advenced/Django-ERP)
![GitHub pull requests](https://img.shields.io/github/issues-pr/AI-Advenced/Django-ERP)

---

## 🌐 Links

- **Website**: [https://Django-ERP.com](https://Django-ERP.com)
- **Documentation**: [https://docs.eerrpp.com](https://docs.Django-ERP.com)
- **GitHub**: [https://github.com/AI-Advenced/EERRPP](https://github.com/AI-Advenced/Django-ERP)
- **Demo**: [https://demo.eerrpp.com](https://demo.Django-ERP.com)
- **Blog**: [https://blog.eerrpp.com](https://blog.Django-ERP.com)

---

<div align="center">

**Made with ❤️ by the EERRPP Team**

⭐ **Star us on GitHub** if you find this project useful!

[⬆ Back to Top](#-enterprise-resource-planning-erp-system)

</div>
