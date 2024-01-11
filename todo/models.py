from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class todo(models.Model):
    title = models.CharField(max_length=100)
    desc  = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    activation_key  = models.CharField(max_length=255, default=1)
    email_validated = models.BooleanField(default=False)

@receiver(post_save, sender=User, dispatch_uid="save_new_user_profile_unique_id")
def save_profile(sender, instance, created, **kwargs):
    user = instance
    if created:
        profile = Profile(user=user)
        profile.save()

def __str__(self):
    return self.user.username


class TodoItem(models.Model):
    task = models.CharField(max_length=200)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.task
