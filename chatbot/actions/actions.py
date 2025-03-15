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


# chatbot/actions/actions.py

class ActionInitiateSecurityAssessment(Action):
    def name(self) -> Text:
        return "action_initiate_security_assessment"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        user_id = tracker.get_slot("user_id")
        if not user_id:
            dispatcher.utter_message("I need to know your user ID to initiate the security assessment.")
            return []

        user = User.objects.get(id=user_id)
        profile = UserProfile.objects.get(user=user)
        
        # Role-specific security assessment questions
        questions = {
            'business_owner': [
                "Do you regularly review the security policies in your organization?",
                "Do you provide security training to your employees?",
                "Do you use multi-factor authentication (MFA) for your business accounts?"
            ],
            'employee': [
                "Do you use strong passwords for your accounts?",
                "Do you report suspicious activities to your IT department?",
                "Do you follow the company's security guidelines?"
            ],
            'it_staff': [
                "Do you perform regular security audits of the network?",
                "Are security patches applied promptly to all systems?",
                "Do you have incident response plans in place?"
            ]
        }

        user_role = profile.role
        user_questions = questions.get(user_role, [])

        # Begin assessment by asking the first question
        if user_questions:
            dispatcher.utter_message(f"Let's begin your security assessment. {user_questions[0]}")
            return [SlotSet("current_question_index", 0)]
        else:
            dispatcher.utter_message("No questions available for your role.")
            return []

class ActionEvaluateSecurityResponse(Action):
    def name(self) -> Text:
        return "action_evaluate_security_response"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Get the current question index
        current_question_index = tracker.get_slot("current_question_index")
        user_response = tracker.latest_message.get("text")

        # Provide immediate feedback based on response
        feedback = self.get_feedback(user_response)
        dispatcher.utter_message(feedback)

        # Update the current question index
        if current_question_index is not None:
            current_question_index += 1
            dispatcher.utter_message(f"Next question: {self.get_next_question(current_question_index)}")
            return [SlotSet("current_question_index", current_question_index)]

        # Assessment is complete; summarize the results
        self.save_assessment(tracker, user_response)
        dispatcher.utter_message("Thank you for completing the assessment. We will send you your results shortly.")
        return []

    def get_next_question(self, index: int) -> str:
        user_role = tracker.get_slot("role")
        questions = {
            'business_owner': [
                "Do you regularly review the security policies in your organization?",
                "Do you provide security training to your employees?",
                "Do you use multi-factor authentication (MFA) for your business accounts?"
            ],
            'employee': [
                "Do you use strong passwords for your accounts?",
                "Do you report suspicious activities to your IT department?",
                "Do you follow the company's security guidelines?"
            ],
            'it_staff': [
                "Do you perform regular security audits of the network?",
                "Are security patches applied promptly to all systems?",
                "Do you have incident response plans in place?"
            ]
        }
        return questions.get(user_role, [])[index] if index < len(questions.get(user_role, [])) else "Assessment complete."

    def get_feedback(self, response: str) -> str:
        # Define feedback based on user response
        if "yes" in response.lower():
            return "Great! You're following good security practices."
        elif "no" in response.lower():
            return "Consider improving this practice to enhance security."
        return "Please provide a clear response (yes/no)."

    def save_assessment(self, tracker: Tracker, response: str):
        user_id = tracker.get_slot("user_id")
        if not user_id:
            return

        score = self.calculate_score(response)
        recommendations = self.generate_recommendations(score)
        risk_level = self.determine_risk_level(score)

        # Save the assessment results in the database
        SecurityAssessment.objects.create(
            user_id=user_id,
            score=score,
            recommendations=recommendations,
            risk_level=risk_level
        )

    def calculate_score(self, response: str) -> float:
        # Placeholder for score calculation logic
        return 80.0 if "yes" in response.lower() else 50.0

    def generate_recommendations(self, score: float) -> list:
        # Placeholder for generating recommendations based on the score
        if score > 75:
            return ["Great job! Keep up the good security practices."]
        elif score > 50:
            return ["Consider improving password management and enabling MFA."]
        else:
            return ["Urgent: Please review your security practices and follow company guidelines."]
        
    def determine_risk_level(self, score: float) -> str:
        # Placeholder for determining the risk level based on the score
        if score > 75:
            return "low"
        elif score > 50:
            return "medium"
        return "high"
