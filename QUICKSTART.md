# Quick Start Guide - Django ERP System

## 🚀 Getting Started in 5 Minutes

### Step 1: Activate Environment
```bash
cd /home/user/webapp
source venv/bin/activate
```

### Step 2: Start the Server
```bash
python manage.py runserver
```

### Step 3: Login
1. Open browser to: http://localhost:8000/
2. Login with:
   - **Username**: admin
   - **Password**: admin123

## 📊 What You Can Do

### Dashboard (Home Page)
- View CRM statistics
- See upcoming activities
- Quick action buttons

### CRM Module

#### 1. Leads
Navigate to **CRM → Leads**
- Click "Add New Lead" button
- Fill in: John Doe, john@example.com, ABC Corp
- Set status: New
- Set source: Website
- Save

#### 2. Contacts
Navigate to **CRM → Contacts**
- Add contact with full details
- Include address information
- Assign to yourself

#### 3. Opportunities
Navigate to **CRM → Opportunities**
- Create a sales opportunity
- Link to a contact
- Set amount: $50,000
- Set stage: Prospecting
- Set probability: 50%

#### 4. Activities
Navigate to **CRM → Activities**
- Schedule a call
- Set due date
- Assign to yourself
- Mark as completed later

### Admin Panel
Navigate to: http://localhost:8000/admin/
- Same login (admin/admin123)
- Manage all data
- View relationships
- Bulk operations

## 🎯 Key Features to Try

### Search & Filter
On any list page:
1. Use search box (top of table)
2. Filter by status/type
3. Click "Filter" button

### Edit Records
1. Click on any record name
2. Or click yellow edit button
3. Make changes
4. Click "Save"

### Delete Records
1. Click red delete button
2. Confirm deletion

### View Statistics
Dashboard shows:
- Total counts
- New records
- Active deals
- Overdue tasks

## 📁 Important Files

### Python (Backend)
- `crm/models.py` - Data models
- `crm/views.py` - Business logic
- `crm/admin.py` - Admin config

### Templates (Frontend)
- `templates/base.html` - Main layout
- `templates/base/index.html` - Dashboard
- `templates/crm/*.html` - CRM pages

### Configuration
- `erp_system/settings.py` - Django settings
- `.env` - Environment variables
- `requirements.txt` - Dependencies

## 🔧 Common Commands

### Database
```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser
```

### Development
```bash
# Run server
python manage.py runserver

# Run on specific port
python manage.py runserver 8080

# Run tests
python manage.py test
```

### Shell
```bash
# Django shell
python manage.py shell

# Example: Query leads
from crm.models import Lead
Lead.objects.all()
```

## 📝 Sample Data Creation

### Using Django Shell
```bash
python manage.py shell
```

```python
from crm.models import Lead, Contact, Opportunity
from users.models import User

# Get admin user
admin = User.objects.get(username='admin')

# Create a lead
lead = Lead.objects.create(
    first_name='Jane',
    last_name='Smith',
    email='jane@company.com',
    company='Tech Corp',
    status='new',
    source='website',
    assigned_to=admin,
    created_by=admin
)

# Create a contact
contact = Contact.objects.create(
    first_name='Bob',
    last_name='Johnson',
    email='bob@example.com',
    company='Big Business Inc',
    contact_type='customer',
    assigned_to=admin,
    created_by=admin
)

# Create an opportunity
opportunity = Opportunity.objects.create(
    name='Website Redesign Project',
    contact=contact,
    amount=75000.00,
    stage='proposal',
    probability=75,
    expected_close_date='2026-03-15',
    assigned_to=admin,
    created_by=admin
)

print("Sample data created!")
```

## 🎨 Customization

### Change Theme Colors
Edit `templates/base.html`, find:
```html
<style>
    .border-left-primary { border-left: 4px solid #4e73df; }
    /* Change color codes here */
</style>
```

### Add New Fields
1. Edit model in `crm/models.py`
2. Add field to model
3. Run `makemigrations`
4. Run `migrate`
5. Update forms in templates

### Change Dashboard Stats
Edit `base/views.py`, modify the `index` function

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Kill process on port 8000
fuser -k 8000/tcp
# Or use different port
python manage.py runserver 8080
```

### Database Locked
```bash
# Exit all Django shells
# Restart server
```

### Static Files Not Loading
```bash
python manage.py collectstatic
```

### Permission Denied
```bash
# Make sure you're in virtual environment
source venv/bin/activate
```

## 📚 Next Steps

1. **Explore Admin Panel**
   - See all models
   - Try bulk actions
   - Use filters

2. **Create Test Data**
   - Add 10 leads
   - Convert some to contacts
   - Create opportunities

3. **Try All CRUD Operations**
   - Create records
   - View details
   - Edit existing
   - Delete test data

4. **Check Relationships**
   - Link activities to leads
   - Track opportunities per contact
   - View activity history

5. **Read Documentation**
   - `README.md` - Full docs
   - `PROJECT_SUMMARY.md` - Technical details
   - Code comments in files

## 💡 Tips

- Use search bars to find records quickly
- Filter lists to focus on specific statuses
- Check dashboard daily for overdue activities
- Assign records to team members
- Use activities to track all interactions
- Convert leads when qualified
- Update opportunity stages regularly

## 🚨 Important Notes

- **Development Only**: This is for development, not production
- **Security**: Change admin password for production
- **Database**: Currently using SQLite (fine for dev)
- **Git**: All code is version controlled

## Need Help?

Check these resources:
- **Django Docs**: https://docs.djangoproject.com/
- **Bootstrap**: https://getbootstrap.com/
- **Project Files**: Read comments in code

Happy coding! 🎉
