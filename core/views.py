"""
Core Application Views & Business Logic (PostgreSQL Connected).
Handles database ORM queries, ManyToMany relationship updates,
and flash messages.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Q
from .models import Project, Profile, Comment


def get_current_user(request):
    """
    Helper to return the authenticated user, or the first available 
    user/superuser if authentication is not yet strictly enforced.
    """
    if request.user.is_authenticated:
        return request.user
    # Fallback to the first superuser/user in the DB so actions work seamlessly
    return User.objects.first()


def discovery_feed(request):
    current_user = get_current_user(request)

    if request.method == 'POST':
        action = request.POST.get('action')
        project_id = request.POST.get('project_id')
        project = get_object_or_404(Project, id=project_id)

        if action == 'like':
            # Toggle like state
            if current_user in project.likes.all():
                project.likes.remove(current_user)
                messages.info(request, f"Unliked '{project.title}'.")
            else:
                project.likes.add(current_user)
                messages.success(request, f"You liked '{project.title}'!")

        elif action == 'join':
            if current_user in project.collaborators.all():
                messages.info(request, f"You are already on the team for '{project.title}'.")
            else:
                project.collaborators.add(current_user)
                messages.success(request, f"You joined the team for '{project.title}'!")

        elif action == 'comment':
            content = request.POST.get('comment_content', '').strip()
            if content:
                Comment.objects.create(
                    project=project,
                    author=current_user,
                    content=content
                )
                messages.success(request, "Comment posted successfully!")

        return redirect('discovery_feed')

    # Prefetch related data for optimal PostgreSQL performance
    projects = Project.objects.prefetch_related(
        'collaborators', 
        'likes', 
        'comments__author'
    ).select_related('creator').all()

    context = {
        'projects': projects,
        'current_user': current_user,
    }
    return render(request, 'core/discovery.html', context)


def project_detail(request, project_id):
    project = get_object_or_404(
        Project.objects.prefetch_related('collaborators', 'comments__author').select_related('creator'),
        id=project_id
    )
    return render(request, 'core/project_detail.html', {'project': project})


def profile_view(request):
    current_user = get_current_user(request)
    
    # Guard against None to satisfy the VS Code type analyzer
    if not current_user:
        messages.error(request, "No active user found.")
        return redirect('discovery_feed')

    profile, _ = Profile.objects.get_or_create(user=current_user)

    if request.method == 'POST':
        name = request.POST.get('name')
        role = request.POST.get('role')
        bio = request.POST.get('bio')

        if name:
            current_user.first_name = name.strip()
            current_user.save()

        if role:
            profile.role = role.strip()
        if bio:
            profile.bio = bio.strip()
        profile.save()

        messages.success(request, "Profile updated successfully!")
        return redirect('profile')

    my_projects = Project.objects.filter(
        Q(creator=current_user) | Q(collaborators=current_user)
    ).distinct()

    context = {
        'profile': profile,
        'my_projects': my_projects,
    }
    return render(request, 'core/profile.html', context)