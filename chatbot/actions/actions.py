from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, AllSlotsReset
import requests
from django.core.cache import cache
from django.contrib.auth.models import User
from .services.openai_service import OpenAIService

class ActionGetProgress(Action):
    def name(self) -> Text:
        return "action_get_progress"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        user_id = tracker.get_slot("user_id")
        if not user_id:
            dispatcher.utter_message("I need to know your user ID to show your progress.")
            return []

        progress = UserProgress.objects.get(user_id=user_id)
        dispatcher.utter_message(
            f"Current Module: {progress.current_module}\n"
            f"Progress: {progress.progress_percentage}%\n"
            f"Completed Modules: {', '.join(progress.completed_modules)}"
        )
        return []

class ActionGetRecommendations(Action):
    def name(self) -> Text:
        return "action_get_recommendations"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        user_id = tracker.get_slot("user_id")
        if not user_id:
            dispatcher.utter_message("I need to know your user ID to provide recommendations.")
            return []

        openai_service = OpenAIService()
        context = openai_service.get_context(User.objects.get(id=user_id))
        
        prompt = (
            f"Based on the user's profile ({context['role']} in {context['industry']} "
            f"with {context['company_size']} employees), recommend the next 3 learning modules "
            "that would be most beneficial for their security education, considering their "
            f"current progress in {context['current_module']}."
        )

        recommendations = openai_service.get_response(prompt, User.objects.get(id=user_id))
        dispatcher.utter_message(recommendations)
        return []

class ActionInitiateTraining(Action):
    def name(self) -> Text:
        return "action_initiate_training"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        user_id = tracker.get_slot("user_id")
        if not user_id:
            dispatcher.utter_message("I need to know your user ID to initiate training.")
            return []

        user = User.objects.get(id=user_id)
        profile = UserProfile.objects.get(user=user)
        
        dispatcher.utter_message(
            f"Welcome {profile.role}! Let's begin your personalized security training."
            f"\nYour industry: {profile.industry}"
            f"\nCompany size: {profile.company_size}"
        )
        
        return []