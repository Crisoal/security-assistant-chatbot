# security_assistant/urls.py

from django.contrib import admin
from django.urls import path, include
from users.views import home_view  # Import home view

urlpatterns = [
    path('', home_view, name='home'),  # Set home as the root URL
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),  # Include user authentication URLs
    path('chatbot/', include('chatbot.urls'))  # Add this line to include chatbot URLs
]
