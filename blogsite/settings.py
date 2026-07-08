from pathlib import Path
from decouple import config

# ──────────────────────────────
# PATHS
# ──────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent


# ──────────────────────────────
# SECURITY
# ──────────────────────────────
SECRET_KEY = config('SECRET_KEY')
DEBUG       = config('DEBUG', default=False, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost').split(',')
CSRF_TRUSTED_ORIGINS = ['https://web-production-57468.up.railway.app']

# ──────────────────────────────
# APPLICATIONS
# ──────────────────────────────
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'myapp',
]


# ──────────────────────────────
# MIDDLEWARE
# ──────────────────────────────
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # serves static files
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


# ──────────────────────────────
# URLS & WSGI
# ──────────────────────────────
ROOT_URLCONF      = 'blogsite.urls'
WSGI_APPLICATION  = 'blogsite.wsgi.application'


# ──────────────────────────────
# TEMPLATES
# ──────────────────────────────
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


# ──────────────────────────────
# DATABASE
# ──────────────────────────────
DATABASES = {
    'default': dj_database_url.config(
        default=f'sqlite:///{BASE_DIR / "db.sqlite3"}'
    )
}
# ──────────────────────────────
# PASSWORD VALIDATION
# ──────────────────────────────
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# ──────────────────────────────
# INTERNATIONALISATION
# ──────────────────────────────
LANGUAGE_CODE = 'en-us'
TIME_ZONE     = 'UTC'
USE_I18N      = True
USE_TZ        = True


# ──────────────────────────────
# STATIC FILES
# ──────────────────────────────
STATIC_URL        = 'static/'
STATICFILES_DIRS  = [BASE_DIR / 'myapp' / 'static']
STATIC_ROOT       = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# ──────────────────────────────
# MEDIA FILES
# ──────────────────────────────
MEDIA_URL  = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


# ──────────────────────────────
# AUTH REDIRECTS
# ──────────────────────────────
LOGIN_URL           = '/blog/login/'
LOGIN_REDIRECT_URL  = '/blog/'
LOGOUT_REDIRECT_URL = '/blog/'


# ──────────────────────────────
# MISCELLANEOUS
# ──────────────────────────────
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'