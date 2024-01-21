from . import views
from django.urls import path, include
from .views import GoogleLoginView

app_name = ''

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('auth/', include('social_django.urls', namespace='social')),
    path('login/google/<str:backend>', GoogleLoginView, name='google_login'),
]