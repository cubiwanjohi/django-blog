# Django Blog

A full-featured blog application built with Django, featuring user authentication, comments, categories, tags, search, and an admin panel.

---

## Features

- **Posts** — create, publish, archive blog posts with featured images
- **Categories & Tags** — organise posts with categories and multiple tags
- **Comments** — logged-in and guest comments with moderation and nested replies
- **Search** — search posts by title, body, or excerpt
- **User Auth** — register, login, logout, and profile page
- **Admin Panel** — full Django admin with bulk actions and filters
- **SEO** — meta title, meta description, and date-based URLs
- **Pagination** — paginated post list, category, tag, and search pages

---

## Tech Stack

- **Backend** — Python 3, Django
- **Database** — SQLite (development)
- **Frontend** — HTML, CSS (custom)
- **Auth** — Django built-in auth system

---

## Project Structure

```
django-blog/
├── blogsite/               # Project settings
│   ├── settings.py
│   └── urls.py
├── myapp/                  # Main blog app
│   ├── migrations/
│   ├── static/
│   │   └── blog/
│   │       ├── css/
│   │       │   └── style.css
│   │       └── js/
│   │           └── main.js
│   ├── templates/
│   │   └── blog/
│   │       ├── base.html
│   │       ├── post_list.html
│   │       ├── post_detail.html
│   │       ├── category_detail.html
│   │       ├── tag_detail.html
│   │       ├── search.html
│   │       ├── register.html
│   │       ├── login.html
│   │       └── profile.html
│   ├── admin.py
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
├── manage.py
├── requirements.txt
└── README.md
```

---

## Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/django-blog.git
cd django-blog
```

### 2. Create and activate a virtual environment
```bash
python3 -m venv env
source env/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Apply migrations
```bash
python manage.py migrate
```

### 5. Create a superuser
```bash
python manage.py createsuperuser
```

### 6. Run the development server
```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/blog/` in your browser.

---

## URLs

| URL | Description |
|---|---|
| `/blog/` | All published posts |
| `/blog/<year>/<month>/<day>/<slug>/` | Single post |
| `/blog/category/<slug>/` | Posts by category |
| `/blog/tag/<slug>/` | Posts by tag |
| `/blog/search/` | Search posts |
| `/blog/register/` | Register account |
| `/blog/login/` | Login |
| `/blog/logout/` | Logout |
| `/blog/profile/` | User profile |
| `/admin/` | Django admin panel |

---

## Environment Variables

Before deploying, move sensitive settings to a `.env` file:

```
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=yourdomain.com
```

---

## Generate `requirements.txt`

```bash
pip freeze > requirements.txt
```

---

## License

MIT License — free to use and modify.