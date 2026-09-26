from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import Profile, Project, Comment

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role')

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'creator', 'progress', 'timeline', 'created_at')
    search_fields = ('title', 'description')
    list_filter = ('timeline', 'created_at')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'project', 'created_at')