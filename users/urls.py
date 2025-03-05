# users/urls.py

from django.urls import path
from .views import signup_view, login_view, logout_view, dashboard_view, home_view
from django.contrib.auth import views as auth_views
from django.urls import path, include


urlpatterns = [
    path('', home_view, name='home'),  # Home page
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('chatbot/', include('chatbot.urls')),
]
