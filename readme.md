# 🏫 Student Marks Management System

A Django-based web application for managing student marks with authentication, subject management, and mark editing capabilities. Designed for scalability, maintainability, and ease of use.

---

## 🚀 Features

- ✅ User Authentication (Login & Logout)
- ✅ Add/Update Student Marks per Subject
- ✅ Prevents Duplicate Entries (based on student + subject)
- ✅ Edit/Delete Marks with Confirmation
- ✅ Toast Notifications (Top Right)
- ✅ Logger for Important Actions
- ✅ Responsive UI using Bootstrap
- ✅ UUID-based models for security
- ✅ AJAX Support for Dynamic Updates

---

## 📁 Project Structure

teacher_portal/
├── portal/
│ ├── migrations/
│ ├── static/
│ ├── templates/
│ ├── models.py
│ ├── views.py
│ ├── forms.py
│ ├── urls.py
│ └── ...
├── manage.py
└── teacher_portal/
├── settings.py
├── urls.py
└── wsgi.py



## ⚙️ Installation & Setup

1. **Clone the repository**


---

## ⚙️ Setup Instructions

```bash
# Clone the repo
git clone https://github.com/Arunchandranvk/teacher-portal.git
cd student-marks-management

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Apply migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Start the server
python manage.py runserver


Visit: http://127.0.0.1:8000/
Login using your superuser credentials.