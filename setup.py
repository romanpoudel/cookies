#!/usr/bin/env python
"""
Setup script for the Django backend
Creates a test user and initializes the database
"""

from django.core.management import execute_from_command_line
from django.contrib.auth.models import User
import os
import sys
import django

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cookie_test.settings')
django.setup()


def create_test_user():
    """Create a test user if it doesn't exist"""
    try:
        user = User.objects.get(username='testuser')
        print(f"Test user '{user.username}' already exists")
    except User.DoesNotExist:
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        print(f"Created test user: {user.username}")
        print("Username: testuser")
        print("Password: testpass123")


def main():
    """Main setup function"""
    print("Setting up Django backend...")

    # Run migrations
    print("Running migrations...")
    execute_from_command_line(['manage.py', 'migrate'])

    # Create test user
    print("Creating test user...")
    create_test_user()

    print("\nSetup complete!")
    print("You can now run: python manage.py runserver 0.0.0.0:8000")


if __name__ == '__main__':
    main()
