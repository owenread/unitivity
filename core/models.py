from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Database object schema

# Defining the profile class
class Profile(models.Model):
    """Extends the default Django User model with application-specific attributes."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=120, default='Developer / Collaborator')
    bio = models.TextField(blank=True, default='Passionate software builder.')

    def __str__(self):
        return f"{self.user.username}'s Profile"


# Auto-create or update Profile whenever a User is created
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        instance.profile.save()

# Defining the profile class
class Project(models.Model):
    """Core Project entity representing collaborative initiatives."""
    title = models.CharField(max_length=200)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_projects')
    description = models.TextField()
    timeline = models.CharField(max_length=100, default='Phase 1: Planning')
    progress = models.PositiveSmallIntegerField(default=0)  # 0 to 100%
    collaborators = models.ManyToManyField(User, related_name='joined_projects', blank=True)
    likes = models.ManyToManyField(User, related_name='liked_projects', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    @property
    def total_likes(self):
        return self.likes.count()

# Defining the comment class
class Comment(models.Model):
    """Discussion comments attached to projects."""
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Comment by {self.author.username} on {self.project.title}"