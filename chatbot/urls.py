# chatbot/urls.py

from django.urls import path
from .views import chatbot_response

urlpatterns = [
    path('response/', chatbot_response, name='chatbot-response'),
]
