# chatbot/actions/actions.py

import logging
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from django.contrib.auth.models import User
from chatbot.models import UserProgress
from chatbot.services.gemini_service import GeminiService

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

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

        try:
            progress = UserProgress.objects.get(user_id=user_id)
            logger.debug(f"User Progress Found: {progress}")
            dispatcher.utter_message(
                f"Current Module: {progress.current_module}\n"
                f"Progress: {progress.progress_percentage}%\n"
                f"Completed Modules: {', '.join(progress.completed_modules)}"
            )
        except UserProgress.DoesNotExist:
            logger.warning(f"No progress found for user_id={user_id}")
            dispatcher.utter_message("No progress found for your account.")
        except Exception as e:
            logger.error(f"Error fetching user progress: {e}")
            dispatcher.utter_message("An error occurred while fetching your progress.")

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

        gemini_service = GeminiService()
        context = gemini_service.get_context(User.objects.get(id=user_id))

        prompt = (
            f"Based on the user's profile ({context['role']} in {context['industry']} "
            f"with {context['company_size']} employees), recommend the next 3 learning modules "
            "that would be most beneficial for their security education, considering their "
            f"current progress in {context['current_module']}."
        )

        recommendations = gemini_service.get_response(prompt, User.objects.get(id=user_id))
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