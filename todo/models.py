from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.contrib.auth import get_user_model

class Regular_todo_list(models.Model):
    task = models.CharField(max_length=300)
    FREQUENCY_LEVEL = [
        ('Daily', 'Daily'),
        ('Weekly', 'Weekly'),
        ('Monthly', 'Monthly'),
    ]
    
    frequency = models.CharField(max_length=30, choices=FREQUENCY_LEVEL, default='Daily')
    completed = models.BooleanField(default=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def save(self, *args, **kwargs):
        if self.author_id is None:
            self.author = get_user_model().objects.first()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.task
    
class Urgent_todo_list(models.Model):
    task = models.CharField(max_length=300)
    due_date = models.DateTimeField()
    completed = models.BooleanField(default=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def time_remaining(self):
        now = timezone.now()
        time_difference = self.due_date - now
        return time_difference
    
    def save(self, *args, **kwargs):
        if not self.author_id:
            self.author = get_user_model().objects.first()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.task
    
    def has_task_on_date(self, check_date):
        return self.due_date.date() == check_date.date()
    
class Completed_todo_list(models.Model):
    REGULAR = 'Regular'
    URGENT= 'Important'
    TASK_TYPES_CHOICES = [
        (REGULAR, 'Regular'),
        (URGENT, 'Urgent'),
    ]
    
    task = models.CharField(max_length=300)
    task_types = models.CharField(max_length=50, choices=TASK_TYPES_CHOICES, null=True, blank=True)
    frequency = models.CharField(max_length=50, choices=Regular_todo_list.FREQUENCY_LEVEL, null=True, blank=True)
    due_date = models.DateTimeField(null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def save(self, *args, **kwargs):
        if not self.author_id and kwargs.get('user'):
            self.author = kwargs['user']
        super().save(*args, **kwargs)
    
    # Add the task from urgent_todo_list & Add the task from regular_todo_list
    @classmethod
    def move_task(cls, urgent_todo=None, regular_todo=None):        #cls = class
        if urgent_todo:
            cls.objects.create(task=urgent_todo.task, task_types=cls.URGENT, due_date=urgent_todo.due_date, author=urgent_todo.author)
        elif regular_todo:
            cls.objects.create(task=regular_todo.task, task_types=cls.REGULAR, frequency=regular_todo.frequency, author=regular_todo.author)
    
    # Restore task from Completed_todo_list to Regular_todo_list
    @classmethod
    def restore_tasks(cls):
        current_time = timezone.now()
        if current_time.hour == 0 and current_time.minute == 1:
            completed_tasks = cls.objects.all()
            for task in completed_tasks:
                Regular_todo_list.objects.create(task=task.task)
                task.delete()
            
    def __str__(self):
        return self.task

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    activation_key  = models.CharField(max_length=255, default=1)
    email_validated = models.BooleanField(default=False)
    
    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User, dispatch_uid="save_new_user_profile_unique_id")
def save_profile(sender, instance, created, **kwargs):
    user = instance
    if created:
        profile = Profile(user=user)
        profile.save()

def __str__(self):
    return self.user.username
