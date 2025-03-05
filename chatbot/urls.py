# chatbot/urls.py

from django.urls import path
from .views import chatbot_response

urlpatterns = [
    path('respond/', chatbot_response, name='chatbot-response'),
]


