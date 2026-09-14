"""
Core Application Views & Business Logic.
Handles template rendering, state manipulation, in-memory data filtering, 
and user interaction via POST forms and flash notifications.
"""

from django.shortcuts import render, redirect
from django.contrib import messages

# In-memory mock database simulating dynamic persistence across HTTP requests
PROJECTS = [
    {
        'id': 1,
        'title': 'EcoTrack App',
        'creator': 'Owen Read',
        'description': 'A mobile application to track daily carbon footprint, discover sustainable habits, and trade eco-tips with neighbors.',
        'likes': 12,
        'progress': '75%',
        'timeline': 'Phase 3: Beta Testing',
        'collaborators': ['Gloria', 'Alex']
    },
    {
        'id': 2,
        'title': 'Subaru Diagnostic Telemetry Tool',
        'creator': 'David Read',
        'description': 'An open-source desktop and web utility designed for reading, visual charting, and analyzing WRX engine telemetry logs.',
        'likes': 8,
        'progress': '40%',
        'timeline': 'Phase 2: Prototyping',
        'collaborators': ['Sam', "Jared", "Linda"]
    },
    {
        'id': 3,
        'title': 'Community Garden Exchange',
        'creator': 'Sarah Jenkins',
        'description': 'A localized marketplace connecting suburban produce growers with local food pantries and community kitchens.',
        'likes': 15,
        'progress': '90%',
        'timeline': 'Phase 4: Launch Prep',
        'collaborators': ['Marcus', 'Elena']
    }
]

# Single-user mock profile dictionary
USER_PROFILE = {
    'name': 'Owen Read',
    'role': 'Full-Stack Developer & Escalations Specialist',
    'bio': 'Passionate software engineering student building clean, user-focused web tools and exploring Python web frameworks.',
}


def discovery_feed(request):
    """
    Renders the main project feed.
    Processes POST form requests to update like counts or join project teams,
    triggering visual user feedback via Django's messaging system.
    """
    if request.method == 'POST':
        action = request.POST.get('action')
        
        # Safely extract and cast project ID from POST payload
        try:
            project_id = int(request.POST.get('project_id'))
        except (TypeError, ValueError):
            project_id = None

        # Search for target project dictionary in data list
        for proj in PROJECTS:
            if proj['id'] == project_id:
                if action == 'like':
                    proj['likes'] += 1
                    messages.success(request, f"You liked '{proj['title']}'!")
                elif action == 'join':
                    # Append active user to project team if not already listed
                    if USER_PROFILE['name'] not in proj['collaborators']:
                        proj['collaborators'].append(USER_PROFILE['name'])
                        messages.success(request, f"You joined the team for '{proj['title']}'!")
                    else:
                        messages.info(request, f"You are already a collaborator on '{proj['title']}'.")
                break

    context = {
        'projects': PROJECTS,
        'user_name': USER_PROFILE['name'],
    }
    return render(request, 'core/discovery.html', context)


def project_detail(request, project_id):
    """
    Lookup and render detailed view for a single project based on integer parameter matching.
    """
    target_project = None
    for proj in PROJECTS:
        if proj['id'] == project_id:
            target_project = proj
            break

    context = {
        'project': target_project
    }
    return render(request, 'core/project_detail.html', context)


def profile_view(request):
    """
    Renders the user profile page.
    Handles bio and name update POST forms and filters projects related to the current user.
    """
    if request.method == 'POST':
        new_name = request.POST.get('name')
        new_bio = request.POST.get('bio')
        
        if new_name:
            USER_PROFILE['name'] = new_name
        if new_bio:
            USER_PROFILE['bio'] = new_bio
            
        messages.success(request, "Profile information updated successfully!")

    # Dynamic filter: Selects projects where the user is either the creator or listed in collaborators
    user_projects = [
        proj for proj in PROJECTS 
        if proj['creator'] == USER_PROFILE['name'] or USER_PROFILE['name'] in proj['collaborators']
    ]

    context = {
        'profile': USER_PROFILE,
        'my_projects': user_projects
    }
    return render(request, 'core/profile.html', context)