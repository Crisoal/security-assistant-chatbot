# chatbot/views.py

import logging
import json
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from chatbot.services.gemini_service import GeminiService
from chatbot.models import ChatMessage
from chatbot.models import UserProgress

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@login_required
@csrf_protect
def chatbot_response(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request method"}, status=405)
    
    try:
        data = json.loads(request.body)
        user_message = data.get("message", "")
        
        if not user_message:
            logger.warning("No message provided in chatbot request.")
            return JsonResponse({"error": "No message provided"}, status=400)
            
        # Role-specific greetings and progress tracking
        role_greetings = {
            'business_owner': "Welcome back, Business Owner!",
            'employee': "Hi again, Employee!",
            'technical_staff': "Greetings, Technical Staff!"
        }
        
        greeting = f"{role_greetings.get(request.user.role, 'Welcome back!')} "
        progress_percentage = get_user_progress_percentage(request.user)
        greeting += f"Your security training progress: {progress_percentage}"
        
        # Process the actual message
        gemini_service = GeminiService()
        response_data = {
            'response': gemini_service.get_response(user_message, request.user)
        }
        return JsonResponse(response_data)
        
    except json.JSONDecodeError:
        return JsonResponse(
            {"error": "Invalid JSON format"},
            status=400
        )
    except Exception as e:
        logger.error(f"Chatbot error: {str(e)}")
        return JsonResponse(
            {"error": "Internal server error"},
            status=500
        )
    
def get_user_progress_percentage(user):
    # Implement your progress calculation logic here
    # For demonstration purposes, assume progress is stored in UserProgress model
    try:
        progress = UserProgress.objects.get(user=user)
        return f"{progress.progress_percentage}%"
    except UserProgress.DoesNotExist:
        return "0%"

@login_required
@csrf_protect
def get_messages(request):
    if request.method != "GET":
        return JsonResponse({"error": "Invalid request method"}, status=405)

    try:
        messages = list(ChatMessage.objects.filter(user=request.user)
                        .order_by('-timestamp').values('message', 'sender', 'timestamp'))

        logger.debug(f"Fetched {len(messages)} chat messages for user {request.user.id}")
        return JsonResponse({"messages": messages})

    except Exception as e:
        logger.error(f"Error fetching chat messages: {e}")
        return JsonResponse({"error": str(e)}, status=500)
