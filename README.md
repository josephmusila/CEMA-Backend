**Features**
- Program Management: Create and list health programs with name, description, creation date, and associated doctor.

- Client Management: Register clients, enroll them in programs, and view detailed profiles (personal info and enrollments).

- Authentication: Token-based authentication for doctors, with group-based permissions (Doctor group).

- API: RESTful endpoints for programs, clients, enrollments, and authentication.

**Technologies**
- Django: ^4.2 (Python web framework)

- Django REST Framework: ^3.14 (API toolkit for Django)

- Python: >=3.8 (Programming language)

- SQLite: Default database (configurable to PostgreSQL or others)

- django-cors-headers: ^4.0 (CORS support for frontend integration)

- djangorestframework-simplejwt: ^5.2 (JWT-based authentication)

**Prerequisites**
- Python: Install Python (>=3.8) from python.org.

- pip: Included with Python or install separately.

- Git: For cloning the repository.

- Frontend: A running React frontend (see frontend README for setup). Assumed to be at http://localhost:3000.

**Installation**

clone repository
```shell
git clone https://github.com/your-repo/health-system-backend.git
cd health-system-backend
```

create virtual enviroment
```shell
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```
Install Dependencies
```shell
pip install -r requirements.txt
```
Apply Migrations
```shell
python manage.py makemigrations
python manage.py migrate
```
Start the Server

```shell
python manage.py runserver
```

