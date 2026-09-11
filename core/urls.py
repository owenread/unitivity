from django.urls import path
from . import views

urlpatterns = [
    path('', views.discovery_feed, name='discovery'),
    path('project/<int:project_id>/', views.project_detail, name='project_detail'),
    path('profile/', views.user_profile, name='profile'),
]