from . import views
from django.urls import path, include
from django.conf.urls import handler404, handler500

app_name = ''

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('activate/<uidb64>/<token>', views.activate, name='activate')
]