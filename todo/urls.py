from . import views
from django.urls import path

app_name = ''

urlpatterns = [
    path('todo_list/', views.todo_list, name='todo_list'),
    path('todo_list/<str:task_type>/<int:todo_id>/', views.delete_todo, name='delete_todo'),
    path('myList/download_mylist_pdf', views.download_mylist_pdf, name='download_mylist_pdf'),
    path('todo_list/data_calendar', views.data_calendar, name='data_calendar'),
]