# 💌 SueweetStay - Fullstack Project

A full-stack Airbnb-inspired web application built for **learning and portfolio purposes**.

- **Frontend:** React + TypeScript + Chakra UI
- **Backend:** Django + Django REST Framework
- **DevOps:** Docker Compose, Render deployment

---

## ✨ Features

- 🔐 User authentication (Email, GitHub, Kakao social login)
- 🏠 Browse accommodation and experience listings
- 🗓 Book rooms and experiences
- 📝 Leave reviews
- 📱 Responsive, mobile-friendly design
- 🔢 Type-safe frontend development with TypeScript
- 🔍 GraphQL API support
- 🔒 Multiple authentication methods (JWT, Token, Session)
- 📊 Real-time error monitoring with Sentry
- ☁️ Media file management with Cloudflare Images

---

## 🛠️ Tech Stack

### 💻 Backend

- Django 5.0.4
- Django REST Framework
- PostgreSQL (for production)
- Cloudflare Images (for media uploads)
- Sentry (error monitoring)
- GraphQL with Strawberry
- JWT & Token Authentication

### 🌐 Frontend

- React 18
- TypeScript
- Chakra UI
- React Query
- React Router v6
- Axios

### ⚙️ DevOps

- Docker / Docker Compose
- Render (Deployment)
- Environment Variables for API & OAuth settings

---

## 🛫 Local Development

### 1. Start development servers

```bash
docker compose -f docker-compose.dev.yml up --build
```

- Frontend: [http://127.0.0.1:3000](http://127.0.0.1:3000)
- Backend (API): [http://127.0.0.1:8000](http://127.0.0.1:8000)

### 2. Environment Variables

#### Front end `.env`

```
REACT_APP_GH_CLIENT_ID=your_github_client_id
REACT_APP_KAKAO_CLIENT_ID=your_kakao_client_id
```

#### Back end `.env`

(If using in production)

- Django secret key
- Database connection settings
- Cloudflare API credentials
- Sentry DSN
- Social Login credentials (GitHub, Kakao)

### 3. Production build

```bash
docker compose -f docker-compose.prod.yml up -d --build
```

---

## 📂 Project Structure

```
sueweetstay-fullstack/
├── backend/        # Django backend
│   ├── users/            # Custom user model and authentication
│   ├── rooms/            # Room listings and management
│   ├── experiences/      # Experience listings
│   ├── bookings/         # Booking system
│   ├── reviews/          # Review system
│   ├── wishlists/        # User wishlists
│   ├── direct_messages/  # Messaging system
│   └── medias/           # Media file handling
├── frontend/       # React frontend
│   ├── components/       # Reusable UI components
│   ├── routes/           # Page components
│   ├── lib/              # Utility functions
│   ├── api.ts            # API calls
│   ├── router.tsx        # Routing configuration
│   └── theme.ts          # Chakra UI theme settings
├── docker-compose.dev.yml
├── docker-compose.prod.yml
├── README.md
```

---

## 🔧 Monitoring & Error Tracking

- **Sentry Integration**
  - Real-time error tracking and monitoring
  - User behavior and performance analysis
  - Early detection of issues in production environments

---

## 🔒 Authentication

- **Multiple authentication systems**
  - JWT authentication
  - Token authentication
  - Session authentication
  - Social Login (GitHub, Kakao)

---

## 🚀 Improvements & Challenges

- 📝 **Room Editing**

  - Unified the "Upload Room" and "Edit Room" pages to enhance UX and reduce code duplication.

- 🌄 **Booking System**

  - Created booking mutations and reservation pages for guests and hosts.

- 📚 **Personal Challenge: Experiences Pages**

  - Applied the same structure as Rooms to develop the Experiences feature independently.

- 🔢 **Type-Safe Development**

  - Strictly followed TypeScript best practices across the frontend.

- 🌐 **Responsive UI**
  - Fully responsive design using Chakra UI breakpoints.

---

## 🚧 Deployment

- Hosted via **Render** with custom domain and free SSL certificates.
- PostgreSQL database managed by Render.
- Cloudflare Images for media uploads.

---

## 🙏 Acknowledgments

- Based on [Nomadcoders Airbnb Clone](https://nomadcoders.co/airbnb-clone/lectures/3926)
- Inspired by [Airbnb](https://www.airbnb.com)

---

## 🗒️ Note

- This website is part of my personal portfolio and is intended for educational and non-commercial purposes only.
