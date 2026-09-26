"""
Core Application Views & Business Logic (PostgreSQL Connected).
Full CRUD implementation:
- CREATE: create_project, Comment.objects.create
- READ: discovery_feed, project_detail (with date filtering)
- UPDATE: profile_view, project likes/joins
- DELETE: delete_project, delete_comment
- AGGREGATE: Avg('progress'), Count('id')
"""

from datetime import timedelta
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Q, Avg, Count
from django.utils import timezone
from .models import Project, Profile, Comment


def get_current_user(request):
    if request.user.is_authenticated:
        return request.user
    return User.objects.first()


def discovery_feed(request):
    current_user = get_current_user(request)

    # Handle Comments, Likes, and Joins
    if request.method == 'POST':
        action = request.POST.get('action')
        project_id = request.POST.get('project_id')
        project = get_object_or_404(Project, id=project_id)

        if action == 'like':
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

        elif action == 'delete_comment':
            comment_id = request.POST.get('comment_id')
            comment = get_object_or_404(Comment, id=comment_id)
            if comment.author == current_user or (current_user and current_user.is_superuser):
                comment.delete()
                messages.success(request, "Comment deleted.")
            else:
                messages.error(request, "You can only delete your own comments.")

        return redirect('discovery_feed')

    # READ / QUERY: With Date Range Filtering
    projects_query = Project.objects.prefetch_related(
        'collaborators', 
        'likes', 
        'comments__author'
    ).select_related('creator')

    filter_days = request.GET.get('days')
    if filter_days:
        try:
            cutoff = timezone.now() - timedelta(days=int(filter_days))
            projects_query = projects_query.filter(created_at__gte=cutoff)
        except ValueError:
            pass

    projects = projects_query.all()

    # AGGREGATES: SQL AVG() and COUNT()
    stats = Project.objects.aggregate(
        avg_progress=Avg('progress'),
        total_projects=Count('id')
    )

    context = {
        'projects': projects,
        'current_user': current_user,
        'stats': stats,
        'filter_days': filter_days,
    }
    return render(request, 'core/discovery.html', context)


def create_project(request):
    """CREATE: Form view to insert a new project into PostgreSQL."""
    current_user = get_current_user(request)
    if not current_user:
        messages.error(request, "You must be signed in to create a project.")
        return redirect('discovery_feed')

    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()
        timeline = request.POST.get('timeline', 'Phase 1: Planning').strip()
        try:
            progress = int(request.POST.get('progress', 0))
        except ValueError:
            progress = 0

        if title and description:
            project = Project.objects.create(
                title=title,
                description=description,
                timeline=timeline,
                progress=progress,
                creator=current_user
            )
            messages.success(request, f"Project '{project.title}' published successfully!")
            return redirect('project_detail', project_id=project.pk)
        else:
            messages.error(request, "Title and description are required.")

    return render(request, 'core/create_project.html')


def delete_project(request, project_id):
    """DELETE: Permanently removes a project record from PostgreSQL."""
    current_user = get_current_user(request)
    project = get_object_or_404(Project, id=project_id)

    # Restrict deletion strictly to the project creator or superuser
    if project.creator == current_user or (current_user and current_user.is_superuser):
        title = project.title
        project.delete()
        messages.success(request, f"Project '{title}' was permanently deleted.")
    else:
        messages.error(request, "You do not have permission to delete this project.")

    return redirect('discovery_feed')


def project_detail(request, project_id):
    project = get_object_or_404(
        Project.objects.prefetch_related('collaborators', 'comments__author').select_related('creator'),
        id=project_id
    )
    current_user = get_current_user(request)
    return render(request, 'core/project_detail.html', {
        'project': project,
        'current_user': current_user,
    })


def profile_view(request):
    """UPDATE: Modifies existing user and profile records in PostgreSQL."""
    current_user = get_current_user(request)
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