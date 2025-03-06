# chatbot/views.py

import os
import json
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.conf import settings
from .services.openai_service import OpenAIService

@csrf_exempt
@login_required
def chatbot_response(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request method"}, status=405)

    try:
        data = json.loads(request.body)
        user_message = data.get("message", "")
        
        if not user_message:
            return JsonResponse({"error": "No message provided"}, status=400)

        openai_service = OpenAIService()
        response = openai_service.get_response(user_message, request.user)
        
        return JsonResponse({"response": response})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)