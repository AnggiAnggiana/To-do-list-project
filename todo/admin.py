from django.contrib import admin
from .models import TodoItem

admin.site.register(TodoItem, list_display=['task', 'completed'])

# Register your models here.
