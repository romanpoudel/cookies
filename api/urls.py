from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('logout-public/', views.logout_public, name='logout_public'),
    path('user/', views.user_info, name='user_info'),
    path('test-cookie/', views.test_cookie, name='test_cookie'),
    path('set-custom-cookie/', views.set_custom_cookie, name='set_custom_cookie'),
]
