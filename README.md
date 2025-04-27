# 🍭 SueweetStay

A simple platform to browse, book, and review accommodations.  
This project is built for **learning and portfolio purposes**.

## ✨ Features

- 🔐 User authentication (Email, Social login)
- 🏠 Browse accommodation listings and details
- 📅 Make bookings
- 📝 Leave reviews
- 📱 Responsive design

## 🛠 Tech Stack

### 🖥 Backend

- Django
- Django REST Framework
- PostgreSQL (for production)
- Cloudflare Images (for uploads)

### 🌐 Frontend

- React
- TypeScript
- Chakra UI
- React Query
- React Router

### ⚙️ DevOps

- Docker / Docker Compose
- Render (for deployment)

## 🛫 Local Development

### 1. Start the project

```bash
docker compose -f docker-compose.dev.yml up --build
```

- Frontend: http://127.0.0.1:3000
- Backend (API): http://127.0.0.1:8000

### 2. Production build

```bash
docker compose -f docker-compose.prod.yml up -d --build
```

## 🗂 Project Structure

```
sueweetstay-fullstack/
├── backend/   # Django backend
├── frontend/  # React frontend
├── docker-compose.dev.yml
├── docker-compose.prod.yml
├── README.md
```

## 🚀 Deployment

- Custom domain support
- Free SSL certificates (via Render)
