# Django ERP System

A comprehensive Enterprise Resource Planning system built with Django, featuring complete CRM functionality in English.

## Features

### ✅ Completed Features

- **Complete CRM Module**:
  - ✅ Lead Management (Create, Read, Update, Delete)
  - ✅ Contact Management (Full CRUD operations)
  - ✅ Opportunity Tracking (Sales pipeline management)
  - ✅ Activity Logging (Tasks, calls, meetings, emails)
  - ✅ Search and filter capabilities
  - ✅ Dashboard with statistics
  - ✅ Status tracking and assignment

- **User Management**:
  - ✅ Custom user model with roles
  - ✅ Authentication system
  - ✅ Admin panel integration
  - ✅ User profile management

- **UI/UX**:
  - ✅ Responsive Bootstrap 5 interface
  - ✅ Modern dashboard
  - ✅ FontAwesome icons
  - ✅ Professional forms

### 🚧 Planned Features

- Inventory Management
- Sales Module
- Purchase Orders
- Financial Management
- Reporting & Analytics

## Installation

1. **Clone repository**:
```bash
cd /home/user/webapp
```

2. **Create virtual environment**:
```bash
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

4. **Run migrations**:
```bash
python manage.py migrate
```

5. **Create superuser**:
```bash
python manage.py createsuperuser
# OR use pre-created: username: admin, password: admin123
```

6. **Run development server**:
```bash
python manage.py runserver
```

## Access Information

### Login Credentials (Pre-created)
- **Username**: admin
- **Password**: admin123
- **Email**: admin@example.com

### URLs
- **Main Application**: http://localhost:8000/
- **Admin Panel**: http://localhost:8000/admin/
- **Login Page**: http://localhost:8000/users/login/

## Project Structure

```
webapp/
├── base/                  # Main app (dashboard)
├── crm/                   # CRM module
│   ├── models.py         # Lead, Contact, Opportunity, Activity models
│   ├── views.py          # All CRUD views
│   ├── admin.py          # Admin configuration
│   └── urls.py           # URL routing
├── users/                 # User management
│   └── models.py         # Custom User model
├── inventory/             # Inventory module (placeholder)
├── templates/             # HTML templates
│   ├── base.html         # Base template
│   ├── base/             # Dashboard templates
│   ├── crm/              # CRM templates
│   └── users/            # Login templates
├── erp_system/           # Project settings
│   ├── settings.py       # Configuration
│   └── urls.py           # Main URL routing
└── manage.py             # Django management script
```

## Data Models

### CRM Models

**Lead**
- Personal information (first_name, last_name, email, phone)
- Company details
- Status (new, contacted, qualified, converted, lost)
- Source tracking
- Assignment to users
- Timestamps

**Contact**
- Extended personal information
- Contact type (customer, supplier, partner, other)
- Full address details
- Assignment and notes

**Opportunity**
- Deal name and amount
- Linked to contacts and leads
- Stage tracking (prospecting → closed)
- Probability percentage
- Expected/actual close dates

**Activity**
- Type (call, meeting, email, task, note)
- Status (planned, completed, cancelled)
- Priority levels
- Due dates and completion tracking
- Links to leads, contacts, opportunities

## Tech Stack

- **Backend**: Django 3.2.25
- **Database**: SQLite (development)
- **Frontend**: Bootstrap 5, FontAwesome 6
- **Authentication**: Django built-in
- **Admin**: Django Admin (customized)

## Development Notes

- All text is in English
- Models include proper relationships
- Views use class-based views with mixins
- Templates are Bootstrap 5 responsive
- Forms include validation
- Admin panel fully configured

## Current Status

**Completed Features:**
- ✅ Complete CRM module with all CRUD operations
- ✅ Dashboard with statistics
- ✅ User authentication
- ✅ Custom user model
- ✅ Responsive UI
- ✅ Admin panel integration

**Functional Entry URIs:**
- `/` - Dashboard
- `/crm/leads/` - Lead list
- `/crm/contacts/` - Contact list
- `/crm/opportunities/` - Opportunity list
- `/crm/activities/` - Activity list
- `/admin/` - Admin panel
- `/users/login/` - Login page

## Next Steps

1. Add more CRM templates (detail views, delete confirmations)
2. Implement inventory management module
3. Add sales and purchase modules
4. Create reporting functionality
5. Add data export features
6. Implement email notifications

## Last Updated

2026-01-07

**GitHub Repository**: Not yet pushed
**Deployment Status**: ❌ Development only (local)
