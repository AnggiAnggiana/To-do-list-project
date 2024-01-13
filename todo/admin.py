from django.contrib import admin
from .models import Regular_todo_list
from .models import Urgent_todo_list
from .models import Completed_todo_list

admin.site.register(Regular_todo_list, list_display=['task', 'completed'])
admin.site.register(Urgent_todo_list, list_display=['task', 'due_date', 'completed'])
admin.site.register(Completed_todo_list, list_display=['task'])
