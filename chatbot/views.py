# chatbot/views.py

import openai
import os
import json
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
RASA_SERVER_URL = os.getenv("RASA_SERVER_URL")

@csrf_exempt
def chatbot_response(request):
    if request.method == "POST":
        data = json.loads(request.body)
        user_message = data.get("message", "")

        if not user_message:
            return JsonResponse({"error": "No message provided"}, status=400)

        # Call OpenAI API
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": user_message}]
            )
            bot_reply = response["choices"][0]["message"]["content"]
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

        return JsonResponse({"response": bot_reply})

    return JsonResponse({"error": "Invalid request method"}, status=405)
