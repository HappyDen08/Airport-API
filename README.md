# Airport API Service

A Django REST API service for managing airport operations, including flights, tickets, and user management.

## Features

- User Authentication with JWT
- Airport and Route Management
- Airplane and Flight Management
- Ticket Booking System
- Crew Management
- Admin Dashboard
- API Documentation with Swagger/ReDoc
- Docker Containerization

## Tech Stack

- Python 3.11
- Django 5.2.1
- Django REST Framework
- PostgreSQL
- Docker & Docker Compose
- JWT Authentication
- Swagger/ReDoc for API documentation

## Prerequisites

- Docker and Docker Compose installed
- Git

## Project Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd Aeroport_API
```

2. Create `.env` file in the root directory with the following variables:
```env
POSTGRES_DB=your_db_name
POSTGRES_USER=your_db_user
POSTGRES_PASSWORD=your_db_password
POSTGRES_HOST=db
POSTGRES_PORT=5432
```

3. Build and start the Docker containers:
```bash
docker-compose up --build
```

The API will be available at `http://localhost:8001`

## API Documentation

After starting the project, you can access the API documentation at:
- Swagger UI: `http://localhost:8001/api/doc/swagger/`
- ReDoc: `http://localhost:8001/api/doc/redoc/`

## API Endpoints

### User Management
- `POST /api/user/register/` - Register new user
- `POST /api/user/token/` - Obtain JWT token
- `POST /api/user/token/refresh/` - Refresh JWT token
- `GET /api/user/me/` - Get user profile
- `PUT/PATCH /api/user/me/` - Update user profile

### Airport Operations
- `GET /api/airport/airports/` - List all airports
- `GET /api/airport/flights/` - List all flights
- `GET /api/airport/routes/` - List all routes
- `GET /api/airport/tickets/` - List all tickets
- `POST /api/airport/orders/` - Create new order

## Authentication

The API uses JWT (JSON Web Token) authentication. To access protected endpoints:

1. Obtain token:
```bash
curl -X POST http://localhost:8001/api/user/token/ -d "email=user@example.com&password=password"
```

2. Use the token in requests:
```bash
curl -H "Authorization: Bearer <your-token>" http://localhost:8001/api/user/me/
```

## Running Tests

To run the test suite:

```bash
# Run all tests
docker-compose run --rm airport python manage.py test

# Run specific app tests
docker-compose run --rm airport python manage.py test user.tests
docker-compose run --rm airport python manage.py test airport.tests
```

## Development

1. Code Style
- The project uses flake8 for code style checking
- Run flake8:
```bash
docker-compose run --rm airport flake8
```

2. Making Migrations
```bash
docker-compose run --rm airport python manage.py makemigrations
docker-compose run --rm airport python manage.py migrate
```

3. Creating Superuser
```bash
docker-compose run --rm airport python manage.py createsuperuser
```

## Project Structure

```
Aeroport_API/
├── airport/            # Airport app
│   ├── models.py       # Database models
│   ├── views.py        # API views
│   ├── serializers.py  # Model serializers
│   └── tests.py        # Tests
├── user/               # User management app
│   ├── models.py       # Custom user model
│   ├── views.py        # User views
│   └── tests.py        # User tests
├── airport_api/        # Project settings
├── docker-compose.yml  # Docker compose config
├── Dockerfile         # Docker config
└── requirements.txt   # Python dependencies
```

## Permissions

The API implements different permission levels:
- Anonymous users can only view public information
- Authenticated users can book tickets and manage their profiles
- Admin users have full access to all endpoints

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request
