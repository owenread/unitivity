"""
URL Routing Configuration for the 'core' application.
Maps application routes to specific view functions defined in views.py.
"""

from django.urls import path
from . import views

urlpatterns = [
    # Route: Home / Discovery Feed (http://127.0.0.1:8000/)
    path('', views.discovery_feed, name='discovery_feed'),
    
    # Route: Dynamic Project Detail View (e.g., http://127.0.0.1:8000/project/1/)
    path('project/<int:project_id>/', views.project_detail, name='project_detail'),
    
    # Route: User Profile & Bio Management (http://127.0.0.1:8000/profile/)
    path('profile/', views.profile_view, name='profile'),
]