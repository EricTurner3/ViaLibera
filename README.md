# ViaLibera - Vehicle Logging Application

A comprehensive vehicle logging application built with Django and Vue.js that helps you track your vehicle's maintenance, fuel consumption, and service history.

## Features

- User authentication
- Vehicle management (CRUD operations)
- Fuel consumption tracking
- Service history recording
- Dashboard views
- Timeline view of vehicle history
- Mobile-responsive design

## Tech Stack

- Backend: Django + Django REST Framework
- Frontend: Vue.js
- Database: PostgreSQL
- Authentication: JWT (JSON Web Tokens)

## Setup Instructions

### Backend Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: . .\venv\Scripts\Activate.ps1
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
Create a `.env` file in the root directory with:
```
DEBUG=True
SECRET_KEY=your-secret-key
DATABASE_URL=postgresql://user:password@localhost:5432/vialibera
```

4. Run migrations:
```bash
cd backend
python manage.py migrate
```

5. Create superuser:
```bash
python manage.py createsuperuser
```

6. Run the development server:
```bash
python manage.py runserver
```

### Frontend Setup

1. Install Node.js dependencies:
```bash
cd frontend
npm install
```

2. Run the development server:
```bash
npm run serve
```

## Default Credentials

- Username: admin
- Password: admin123

## API Documentation

The API documentation is available at `/api/docs/` when running the backend server.

## License

GLPv3