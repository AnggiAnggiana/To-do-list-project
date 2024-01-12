from . import views
from django.urls import path
from .views import remove_todo #todo_list

app_name = ''

urlpatterns = [
    path('todo_list/', views.todo_list, name='todo_list'),
    path('todo/<int:todo_id>/', remove_todo, name='remove_todo'),
    path('myList/<int:todo_id>/', views.delete_todo, name='delete_todo'),
    path('myList/download_mylist_pdf', views.download_mylist_pdf, name='download_mylist_pdf'),
]