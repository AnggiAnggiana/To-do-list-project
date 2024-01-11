from django.contrib import admin
from django.urls import include, path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.shortcuts import redirect

urlpatterns = [
    path('accounts/', include('accounts.urls')),
    path('', lambda request: redirect('login'), name='home'),
    path('todo/', include('todo.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
]

urlpatterns += staticfiles_urlpatterns()
