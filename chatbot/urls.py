# chatbot/urls.py

from django.urls import path
from .views import chatbot_response, get_messages

urlpatterns = [
    path('respond/', chatbot_response, name='chatbot-response'),
    path('messages/', get_messages, name='chatbot-messages'),
]

