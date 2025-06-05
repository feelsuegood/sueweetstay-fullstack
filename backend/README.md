# 💌 Sueweetstay - Backend

A Django-based backend for an Airbnb-inspired project, built with Python 3.12 and Django 5.0.4.

## 🚀 Getting Started

### Prerequisites

- Python 3.12
- Poetry (Python package manager)
- Cloudflare account (for media storage)
- GitHub OAuth credentials (for social login)
- Kakao OAuth credentials (for social login)

### Environment Variables

Create a `.env` file in the backend directory with the following variables:

```bash
SECRET_KEY=your_django_secret_key
DEBUG=True  # Set to False in production
GH_ID=your_github_oauth_client_id
GH_SECRET=your_github_oauth_secret
KAKAO_ID=your_kakao_oauth_client_id
CF_TOKEN=your_cloudflare_token
CF_ID=your_cloudflare_account_id
```

### Installation

1. Initialize Poetry and install dependencies

```bash
poetry config virtualenvs.in-project true --local
poetry install
poetry shell
```

2. Create Django project

```bash
django-admin startproject config .
```

3. Initialize database

```bash
python manage.py migrate
python manage.py createsuperuser
```

## 📦 Project Structure

- `users/` - Custom user model and authentication
  - JWT & Token authentication
  - Social login (GitHub, Kakao)
  - Custom user profiles
- `rooms/` - Room listings and management
  - Room categories
  - Amenities
  - Photo management
  - Search and filtering
- `experiences/` - Experience listings
  - Experience categories
  - Perks system
  - Scheduling
- `bookings/` - Booking system
  - Room bookings
  - Experience bookings
  - Availability checking
- `reviews/` - Review system
  - Ratings
  - User reviews
- `wishlists/` - User wishlists
  - Save favorite rooms
  - Save favorite experiences
- `direct_messages/` - Messaging system
  - Chat rooms
  - User-to-user messaging
- `medias/` - Media file handling
  - Cloudflare integration
  - Image upload/management
- `common/` - Shared utilities and configurations
  - Common models
  - Shared utilities
- `categories/` - Category management
  - Room categories
  - Experience categories

## 🔒 Authentication

The project supports multiple authentication methods:
- JWT Authentication
- Token Authentication
- Session Authentication
- Social Login (GitHub, Kakao)

## 🌐 API Endpoints

The API supports both REST and GraphQL:

- REST API endpoints are prefixed with `/api/v1/`
- GraphQL endpoint is available at `/graphql`

See `Url.md` for detailed API endpoints.

## ⚠️ Important Notes

- Custom user model must be implemented at the beginning of the project
- If modifying user model mid-project:
  - Delete database
  - Remove initial migration files (001_initial.py, 002_initial.py)
  - Keep migrations folder and __init__.py

## 🔧 Development

For local development:

```bash
python manage.py runserver
```

For Docker development:

```bash
docker-compose -f docker-compose.dev.yml up
```

## 📚 References

- [Django Documentation](https://docs.djangoproject.com/en/5.0/)
- [Django ORM Documentation](https://docs.djangoproject.com/en/5.1/ref/models/instances/)
- [Django Queries Documentation](https://docs.djangoproject.com/en/5.1/topics/db/queries/)
- [Nomadcoders Airbnb Clone](https://nomadcoders.co/airbnb-clone/lectures/3926)
- [Airbnb](https://www.airbnb.com)
