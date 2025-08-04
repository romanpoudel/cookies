"""
Production settings for Django backend
This file shows the proper configuration for production cookie handling
"""

from .settings import *

# Production settings
DEBUG = False
SECRET_KEY = os.environ.get('SECRET_KEY', 'your-production-secret-key')

# HTTPS settings for production
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# SameSite settings for cross-origin requests
SESSION_COOKIE_SAMESITE = 'None'  # Required for cross-origin
CSRF_COOKIE_SAMESITE = 'None'

# Domain settings for production
ALLOWED_HOSTS = [
    'yourdomain.com',
    'www.yourdomain.com',
    'api.yourdomain.com',
]

# CORS settings for production
CORS_ALLOWED_ORIGINS = [
    "https://yourdomain.com",
    "https://www.yourdomain.com",
    "https://app.yourdomain.com",
]

# Cookie domain for production (include subdomains)
SESSION_COOKIE_DOMAIN = '.yourdomain.com'
CSRF_COOKIE_DOMAIN = '.yourdomain.com'

# Additional security headers
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# Database settings (example for PostgreSQL)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST'),
        'PORT': os.environ.get('DB_PORT', '5432'),
    }
}

# Static files
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'

# Media files
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'
