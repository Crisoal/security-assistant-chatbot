# chatbot/views.py

import logging
import json
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from chatbot.services.gemini_service import GeminiService
from chatbot.models import ChatMessage

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@csrf_protect
@login_required
def chatbot_response(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request method"}, status=405)

    try:
        data = json.loads(request.body)
        user_message = data.get("message", "")

        if not user_message:
            logger.warning("No message provided in chatbot request.")
            return JsonResponse({"error": "No message provided"}, status=400)

        logger.debug(f"Received user message: {user_message}")

        gemini_service = GeminiService()
        response = gemini_service.get_response(user_message, request.user)

        logger.debug(f"Chatbot response: {response}")

        return JsonResponse({"response": response})

    except Exception as e:
        logger.error(f"Error in chatbot_response: {e}")
        return JsonResponse({"error": str(e)}, status=500)

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
