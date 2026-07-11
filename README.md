# 🎬 cineReviews

A full-stack web application built with **Django** that allows users to discover, review and rate movies. The platform includes user authentication, personalized profiles, comments, notifications, following system, and an administration panel for managing movies.

---

## 📖 About

cineReviews is a movie review platform where users can:

- Browse the movie catalog
- Search and filter movies
- View movie details
- Rate and review movies
- Follow other users
- Receive notifications when followed users publish new reviews
- Manage personal profiles

The project also includes role-based permissions, allowing moderators and administrators to manage the platform.

---

## ✨ Features

### 👤 User Features

- User registration and login
- User profile
- Profile picture upload
- Password management
- Follow/unfollow other users
- Notifications system
- View personal reviews

### 🎥 Movie Features

- Browse all movies
- Search by:
  - Title
  - Director
  - Actor
  - Genre
- View detailed movie information
- IMDb score display
- Movie poster upload
- Average rating calculation

### ⭐ Reviews

- Publish movie reviews
- Give a rating
- Edit or remove reviews
- Automatic movie average rating calculation

### 🔐 Administration

Role-based permissions using Django Authentication:

- Administrator
- Moderator
- Regular User

Administrators can:

- Add movies
- Edit movie information
- Upload movie posters
- Manage users

---

## 🛠️ Technologies

- Python
- Django
- SQLite
- HTML5
- CSS3
- JavaScript
- Bootstrap
- Django Authentication System

---

## 📂 Project Structure

```
cineReviews/
│
├── cineReviews/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   ├── wsgi.py
│   └── __init__.py
│
├── filmes/
│   ├── migrations/
│   ├── templates/
│   ├── static/
│   ├── admin.py
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   ├── views.py
│   └── tests.py
│
├── sessao/
│   ├── migrations/
│   ├── templates/
│   ├── static/
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   ├── views.py
│   └── admin.py
│
├── media/
│
├── static/
│
├── templates/
│
├── manage.py
├── requirements.txt
├── README.md
└── .gitignore
```

---

## 🚀 Installation

### 1. Clone the repository

```bash
git clone https://github.com/ClebasS/cineReviews.git
```

### 2. Enter the project

```bash
cd cineReviews
```

### 3. Create a virtual environment

Windows

```bash
python -m venv .venv
```

Activate it

```bash
.venv\Scripts\activate
```

Linux / macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

### 4. Install dependencies

```bash
pip install django
```

or

```bash
pip install -r requirements.txt
```

if available.

---

### 5. Apply migrations

```bash
python manage.py migrate
```

---

### 6. Create an administrator account

```bash
python manage.py createsuperuser
```

---

### 7. Run the development server

```bash
python manage.py runserver
```

Open:

```
http://127.0.0.1:8000/filmes
```

---

## 🔑 User Roles

| Role | Permissions |
|------|-------------|
| User | Browse, review, rate, follow users |
| Moderator | Additional moderation permissions |
| Administrator | Full access to movie and user management |

---

## 📷 Main Functionalities

- User authentication
- Movie management
- Search and filtering
- Reviews and ratings
- Movie poster upload
- Notifications
- Following system
- Permission management
- Responsive interface

---

## 📸 Screenshots

### Home Page

The landing page introduces the platform and showcases the latest movie releases.

![Home Page](screenshots/home.png)

---

### Browse & Search Movies

Users can browse the movie catalog and search by title, actor, director or genre.

![Browse Movies](screenshots/movies.png)

---

### Movie Details

Each movie page displays detailed information including synopsis, cast, genres, IMDb rating, community rating and user reviews.

![Movie Details](screenshots/movie-details.png)

---

### Submit a Review

Authenticated users can rate movies using a 5-star system and optionally leave a written review.

![Review](screenshots/review.png)

---

### User Profile

Users can customize their profile, upload a profile picture, update personal information and select their favourite genres.

![Profile](screenshots/profile.png)

---

### Notifications

Users receive notifications whenever someone they follow publishes a new review.

![Notifications](screenshots/notifications.png)

---

## 🎯 Learning Objectives

This project was developed to practice:

- Django framework
- MVC/MVT architecture
- Authentication and authorization
- CRUD operations
- File uploads
- Database modeling
- Template rendering
- User management
- Web application development

---

## 📄 License

This project was developed for educational purposes.
