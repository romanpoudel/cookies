from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.conf import settings
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
import json
import os


@csrf_exempt
@require_http_methods(["POST"])
def login_view(request):
    """Login endpoint that sets session cookies"""
    try:
        data = json.loads(request.body)
        username = data.get('username', 'testuser')
        password = data.get('password', 'testpass123')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # Set additional custom cookies for testing
            response = JsonResponse({
                'success': True,
                'message': 'Login successful',
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email
                }
            })

            # Set custom cookies with cross-origin compatible settings
            response.set_cookie(
                'auth_token',
                'test-auth-token-123',
                max_age=3600,  # 1 hour
                httponly=True,
                samesite='None',  # 'None' for cross-origin requests
                secure=settings.SESSION_COOKIE_SECURE,  # False for HTTP, True for HTTPS
                domain=None  # None for cross-origin requests
            )

            response.set_cookie(
                'user_preference',
                'dark_mode',
                max_age=86400,  # 24 hours
                httponly=False,  # Allow JavaScript access
                samesite='None',  # 'None' for cross-origin requests
                secure=settings.SESSION_COOKIE_SECURE,  # False for HTTP, True for HTTPS
                domain=None  # None for cross-origin requests
            )

            return response
        else:
            return JsonResponse({
                'success': False,
                'message': 'Invalid credentials'
            }, status=401)

    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'message': 'Invalid JSON'
        }, status=400)


@csrf_exempt
@login_required
def logout_view(request):
    """Logout endpoint that clears cookies"""
    logout(request)

    response = JsonResponse({
        'success': True,
        'message': 'Logout successful'
    })

    # Clear custom cookies with same settings as when they were set
    response.delete_cookie('auth_token', samesite='None',
                           secure=settings.SESSION_COOKIE_SECURE)
    response.delete_cookie('user_preference', samesite='None',
                           secure=settings.SESSION_COOKIE_SECURE)

    return response


@csrf_exempt
def logout_public(request):
    """Public logout endpoint that clears cookies without requiring authentication"""
    logout(request)

    response = JsonResponse({
        'success': True,
        'message': 'Logout successful'
    })

    # Clear custom cookies with same settings as when they were set
    response.delete_cookie('auth_token', samesite='None',
                           secure=settings.SESSION_COOKIE_SECURE)
    response.delete_cookie('user_preference', samesite='None',
                           secure=settings.SESSION_COOKIE_SECURE)

    return response


@api_view(['GET'])
@permission_classes([AllowAny])
def user_info(request):
    """Get current user information - returns JSON instead of redirecting"""
    if request.user.is_authenticated:
        return Response({
            'success': True,
            'user': {
                'id': request.user.id,
                'username': request.user.username,
                'email': request.user.email,
                'is_authenticated': request.user.is_authenticated
            },
            'session_id': request.session.session_key,
            'cookies': dict(request.COOKIES)
        })
    else:
        return Response({
            'success': False,
            'message': 'User not authenticated',
            'is_authenticated': False
        }, status=401)


@api_view(['GET'])
@permission_classes([AllowAny])
def test_cookie(request):
    """Test endpoint to check if cookies are being sent"""
    return Response({
        'success': True,
        'message': 'Cookie test endpoint',
        'received_cookies': dict(request.COOKIES),
        'session_id': request.session.session_key if request.session.session_key else None,
        'is_authenticated': request.user.is_authenticated
    })


@require_http_methods(["POST"])
def set_custom_cookie(request):
    """Set a custom cookie with specific parameters"""
    try:
        data = json.loads(request.body)
        cookie_name = data.get('name', 'custom_cookie')
        cookie_value = data.get('value', 'default_value')
        cookie_max_age = data.get('max_age', 3600)
        cookie_httponly = data.get('httponly', True)
        # Default to 'None' for cross-origin
        cookie_samesite = data.get('samesite', 'None')

        response = JsonResponse({
            'success': True,
            'message': f'Cookie {cookie_name} set successfully',
            'cookie_config': {
                'name': cookie_name,
                'value': cookie_value,
                'max_age': cookie_max_age,
                'httponly': cookie_httponly,
                'samesite': cookie_samesite,
                'secure': settings.SESSION_COOKIE_SECURE
            }
        })

        response.set_cookie(
            cookie_name,
            cookie_value,
            max_age=cookie_max_age,
            httponly=cookie_httponly,
            samesite=cookie_samesite,
            secure=settings.SESSION_COOKIE_SECURE
        )

        return response

    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'message': 'Invalid JSON'
        }, status=400)
