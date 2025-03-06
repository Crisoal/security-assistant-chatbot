import os
import openai
from django.conf import settings
from django.core.cache import cache
from typing import Dict, Any

class OpenAIService:
    def __init__(self):
        openai.api_key = os.getenv("OPENAI_API_KEY")
        self.model = "gpt-4"
        self.cache_timeout = 300  # 5 minutes

    def get_context(self, user: settings.AUTH_USER_MODEL) -> Dict[str, Any]:
        """Generate context for OpenAI based on user profile"""
        profile = UserProfile.objects.get(user=user)
        return {
            "role": profile.role,
            "industry": profile.industry,
            "company_size": profile.company_size,
            "security_level": profile.security_level,
            "current_module": UserProgress.objects.get(user=user).current_module
        }

    def get_response(self, prompt: str, user: settings.AUTH_USER_MODEL) -> str:
        """Get response from OpenAI with caching"""
        cache_key = f"openai_response_{user.id}_{prompt}"
        cached_response = cache.get(cache_key)
        
        if cached_response:
            return cached_response

        context = self.get_context(user)
        prompt = f"{prompt}\n\nContext: {context}"
        
        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=500
            )
            result = response.choices[0].message.content
            cache.set(cache_key, result, self.cache_timeout)
            return result
        except Exception as e:
            return f"Error: {str(e)}"