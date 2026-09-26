"""
URL Routing Configuration for the 'core' application.
Maps application routes to specific view functions defined in views.py.
"""

from django.urls import path
from . import views

urlpatterns = [
    # Route: Home / Discovery Feed (http://127.0.0.1:8000/)
    path('', views.discovery_feed, name='discovery_feed'),
    
    # Route: Start / Create a New Project (http://127.0.0.1:8000/project/new/)
    path('project/new/', views.create_project, name='create_project'),
    
    # Route: Dynamic Project Detail View (e.g., http://127.0.0.1:8000/project/1/)
    path('project/<int:project_id>/', views.project_detail, name='project_detail'),
    
    # Route: Delete Project Record (e.g., http://127.0.0.1:8000/project/1/delete/)
    path('project/<int:project_id>/delete/', views.delete_project, name='delete_project'),
    
    # Route: User Profile & Bio Management (http://127.0.0.1:8000/profile/)
    path('profile/', views.profile_view, name='profile'),
]