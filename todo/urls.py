from . import views
from django.urls import path
from .views import todo_list, remove_todo

app_name = ''

urlpatterns = [
    path('', todo_list, name='todo_list'),
    path('todo/<int:todo_id>/', remove_todo, name='remove_todo'),
    path('myList/<int:todo_id>/', views.delete_todo, name='delete_todo'),
    path('myList/', views.myList, name='myList'),
    path('myList/download_mylist_pdf', views.download_mylist_pdf, name='download_mylist_pdf'),
]