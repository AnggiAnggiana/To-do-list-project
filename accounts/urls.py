from . import views
from django.urls import path

app_name = ''

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('activate/<str:uidb64>/<str:token>', views.activate, name='activate'),
]