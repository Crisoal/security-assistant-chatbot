# services/gemini_service.py

import os
import requests
import json
import logging
from django.conf import settings
from django.core.cache import cache
from typing import Dict, Any
from chatbot.models import UserProfile, UserProgress

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class GeminiService:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
        self.cache_timeout = 300  # 5 minutes

    def get_context(self, user: settings.AUTH_USER_MODEL) -> Dict[str, Any]:
        """Generate context for Gemini API based on user profile"""
        try:
            profile = UserProfile.objects.get(user=user)
            progress = UserProgress.objects.get(user=user)
            logger.debug(f"UserProfile: {profile}, UserProgress: {progress}")
            return {
                "role": profile.role,
                "industry": profile.industry,
                "company_size": profile.company_size,
                "security_level": profile.security_level,
                "current_module": progress.current_module
            }
        except Exception as e:
            logger.error(f"Error fetching user context: {e}")
            return {}

    def get_response(self, prompt: str, user: settings.AUTH_USER_MODEL) -> str:
        """Get response from Google Gemini API with caching"""
        cache_key = f"gemini_response_{user.id}_{prompt}"
        cached_response = cache.get(cache_key)
        if cached_response:
            logger.debug(f"Cache hit for {cache_key}")
            return cached_response

        context = self.get_context(user)
        if not context:
            logger.warning("Context is empty, API call may fail.")

        prompt = f"{prompt}\n\nContext: {context}"

        headers = {"Content-Type": "application/json"}
        payload = {"contents": [{"parts": [{"text": prompt}]}]}

        logger.debug(f"Sending request to Gemini API: {payload}")

        try:
            response = requests.post(
                f"{self.base_url}?key={self.api_key}",
                headers=headers,
                json=payload
            )
            response_data = response.json()
            logger.debug(f"Response from Gemini API: {response_data}")

            # Extract response text
            result = response_data.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "No response")

            # Cache response
            cache.set(cache_key, result, self.cache_timeout)
            return result
        except Exception as e:
            logger.error(f"Error calling Gemini API: {e}")
            return f"Error: {str(e)}"
