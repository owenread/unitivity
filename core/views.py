from django.shortcuts import render, redirect

# In-memory mock data temporarily until we build a functional database in the next two weeks. 
PROJECTS = [
    {
        'id': 1,
        'title': 'EcoTrack App',
        'creator': 'Owen',
        'description': 'A mobile app to track daily carbon footprint and trade eco-tips.',
        'likes': 12,
        'progress': '50%',
        'timeline': 'Phase 2: Beta Testing',
        'collaborators': ['Gloria', 'Alex']
    },
    {
        'id': 2,
        'title': 'Subaru Diagnostic Tool',
        'creator': 'David',
        'description': 'Open-source web tool for reading WRX engine telemetry logs.',
        'likes': 8,
        'progress': '25%',
        'timeline': 'Phase 1: Prototyping',
        'collaborators': ['Sam']
    }
]

USER_PROFILE = {
    'name': 'Owen Read',
    'role': 'Full Stack Developer',
    'bio': 'Building clean web tools and learning Django frameworks.',
}

def discovery_feed(request):
    """
    Page 1: Renders the Discovery Feed listing all project ideas.
    Handles 'Like' and 'Join' POST actions from user interactions.
    """
    if request.method == 'POST':
        project_id = int(request.POST.get('project_id', 0))
        action = request.POST.get('action')
        
        for proj in PROJECTS:
            if proj['id'] == project_id:
                if action == 'like':
                    proj['likes'] += 1
                elif action == 'join' and 'You' not in proj['collaborators']:
                    proj['collaborators'].append('You')
        return redirect('discovery')

    context = {'projects': PROJECTS}
    return render(request, 'core/discovery.html', context)

def project_detail(request, project_id):
    """
    Page 2: Renders detailed project view including progress, timeline, and collaborators.
    """
    project = next((p for p in PROJECTS if p['id'] == project_id), None)
    context = {'project': project}
    return render(request, 'core/project_detail.html', context)

def user_profile(request):
    """
    Page 3: Displays user profile, allows updating bio info, and lists created projects.
    """
    if request.method == 'POST':
        USER_PROFILE['name'] = request.POST.get('name', USER_PROFILE['name'])
        USER_PROFILE['bio'] = request.POST.get('bio', USER_PROFILE['bio'])
        return redirect('profile')

    my_projects = [p for p in PROJECTS if p['creator'] == 'Owen']
    context = {
        'profile': USER_PROFILE,
        'my_projects': my_projects
    }
    return render(request, 'core/profile.html', context)