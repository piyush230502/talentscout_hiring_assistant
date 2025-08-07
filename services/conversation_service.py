"""
Conversation management service for TalentScout Hiring Assistant
"""
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime

from utils.constants import ConversationState, FALLBACK_RESPONSES
from utils.helpers import (
    validate_email, validate_phone, validate_name, 
    is_exit_keyword, clean_text_input, extract_numbers_from_text,
    determine_experience_level, extract_tech_stack
)
from utils.logger import logger, log_conversation_event, log_error
from models.session_state import ConversationContext
from prompts.greeting_prompt import GreetingPrompts
from prompts.info_prompt import InfoCollectionPrompts
from prompts.tech_question_prompt import TechnicalQuestionPrompts
from prompts.fallback_prompt import FallbackPrompts
from services.llm_service import llm_service

class ConversationService:
    """Service for managing conversation flow and state transitions"""

    def __init__(self, session_id: str):
        self.session_id = session_id
        self.context = ConversationContext()
        self.required_fields = ["name", "email", "phone", "experience_years", "tech_stack"]

    def process_user_input(
        self, 
        user_input: str, 
        conversation_history: List[Dict[str, Any]] = None
    ) -> Tuple[str, Dict[str, Any]]:
        """Process user input and return appropriate response with updated context"""

        try:
            # Clean and validate input
            user_input = clean_text_input(user_input)

            # Check for exit keywords
            if is_exit_keyword(user_input):
                return self._handle_exit(), self._get_context_dict()

            # Log conversation event
            log_conversation_event(
                logger, 
                "processing_user_input",
                self.session_id,
                self.context.current_state.value,
                user_input_length=len(user_input)
            )

            # Route to appropriate handler based on current state
            response = self._route_to_handler(user_input, conversation_history or [])

            return response, self._get_context_dict()

        except Exception as e:
            log_error(logger, e, self.session_id, {
                "action": "process_user_input",
                "current_state": self.context.current_state.value
            })

            return FallbackPrompts.get_error_message("general"), self._get_context_dict()

    def _route_to_handler(self, user_input: str, conversation_history: List[Dict[str, Any]]) -> str:
        """Route user input to appropriate state handler"""

        state_handlers = {
            ConversationState.GREETING: self._handle_greeting,
            ConversationState.COLLECTING_NAME: self._handle_name_collection,
            ConversationState.COLLECTING_EMAIL: self._handle_email_collection,
            ConversationState.COLLECTING_PHONE: self._handle_phone_collection,
            ConversationState.COLLECTING_EXPERIENCE: self._handle_experience_collection,
            ConversationState.COLLECTING_TECH_STACK: self._handle_tech_stack_collection,
            ConversationState.GENERATING_QUESTIONS: self._handle_question_generation,
            ConversationState.AWAITING_TECH_ANSWERS: self._handle_tech_answers,
            ConversationState.COMPLETED: self._handle_completed_state,
            ConversationState.ERROR: self._handle_error_state
        }

        handler = state_handlers.get(self.context.current_state)
        if handler:
            return handler(user_input, conversation_history)
        else:
            return FallbackPrompts.get_fallback_response("general", self.context.retry_count)

    def _handle_greeting(self, user_input: str, conversation_history: List[Dict[str, Any]]) -> str:
        """Handle greeting state"""
        # Transition to name collection
        self.context.transition_to(ConversationState.COLLECTING_NAME)
        self.context.set_awaiting_field("name")

        return InfoCollectionPrompts.get_name_prompt()

    def _handle_name_collection(self, user_input: str, conversation_history: List[Dict[str, Any]]) -> str:
        """Handle name collection"""

        if validate_name(user_input):
            # Valid name - store and move to next field
            clean_name = ' '.join(user_input.strip().split())  # Clean up spacing
            self.context.update_collected_data("name", clean_name)
            self.context.transition_to(ConversationState.COLLECTING_EMAIL)
            self.context.set_awaiting_field("email")

            return InfoCollectionPrompts.get_email_prompt(name=clean_name)
        else:
            # Invalid name - retry
            self.context.increment_retry()
            error_type = "empty" if not user_input else "invalid"

            if self.context.retry_count >= 3:
                return FallbackPrompts.get_skip_option_prompt("name")

            return InfoCollectionPrompts.get_validation_error_message("name", error_type)

    def _handle_email_collection(self, user_input: str, conversation_history: List[Dict[str, Any]]) -> str:
        """Handle email collection"""

        if validate_email(user_input):
            # Valid email - store and move to next field
            self.context.update_collected_data("email", user_input.lower().strip())
            self.context.transition_to(ConversationState.COLLECTING_PHONE)
            self.context.set_awaiting_field("phone")

            return InfoCollectionPrompts.get_phone_prompt()
        else:
            # Invalid email - retry
            self.context.increment_retry()
            error_type = "empty" if not user_input else "invalid"

            if self.context.retry_count >= 3:
                return FallbackPrompts.get_skip_option_prompt("email")

            return InfoCollectionPrompts.get_validation_error_message("email", error_type)

    def _handle_phone_collection(self, user_input: str, conversation_history: List[Dict[str, Any]]) -> str:
        """Handle phone collection"""

        if validate_phone(user_input):
            # Valid phone - store and move to next field
            self.context.update_collected_data("phone", user_input.strip())
            self.context.transition_to(ConversationState.COLLECTING_EXPERIENCE)
            self.context.set_awaiting_field("experience_years")

            return InfoCollectionPrompts.get_experience_prompt()
        else:
            # Invalid phone - retry
            self.context.increment_retry()
            error_type = "empty" if not user_input else "invalid"

            if self.context.retry_count >= 3:
                return FallbackPrompts.get_skip_option_prompt("phone")

            return InfoCollectionPrompts.get_validation_error_message("phone", error_type)

    def _handle_experience_collection(self, user_input: str, conversation_history: List[Dict[str, Any]]) -> str:
        """Handle experience collection"""

        # Extract numbers from input
        numbers = extract_numbers_from_text(user_input)

        if numbers and 0 <= numbers[0] <= 50:
            # Valid experience - store and move to next field
            experience_years = numbers[0]
            self.context.update_collected_data("experience_years", experience_years)
            self.context.transition_to(ConversationState.COLLECTING_TECH_STACK)
            self.context.set_awaiting_field("tech_stack")

            return InfoCollectionPrompts.get_tech_stack_prompt(
                experience_years=experience_years
            )
        else:
            # Invalid experience - retry
            self.context.increment_retry()

            if not numbers:
                error_type = "empty" if not user_input else "invalid"
            elif numbers[0] < 0:
                error_type = "negative"
            else:
                error_type = "too_high"

            if self.context.retry_count >= 3:
                return FallbackPrompts.get_skip_option_prompt("experience")

            return InfoCollectionPrompts.get_validation_error_message("experience", error_type)

    def _handle_tech_stack_collection(self, user_input: str, conversation_history: List[Dict[str, Any]]) -> str:
        """Handle tech stack collection"""

        if len(user_input.strip()) >= 3:  # Minimum length validation
            # Valid tech stack - store and move to question generation
            self.context.update_collected_data("tech_stack", user_input.strip())
            self.context.transition_to(ConversationState.GENERATING_QUESTIONS)

            return self._generate_technical_questions()
        else:
            # Invalid tech stack - retry
            self.context.increment_retry()
            error_type = "empty" if not user_input else "too_short"

            if self.context.retry_count >= 3:
                return FallbackPrompts.get_skip_option_prompt("tech_stack")

            return InfoCollectionPrompts.get_validation_error_message("tech_stack", error_type)

    def _handle_question_generation(self, user_input: str, conversation_history: List[Dict[str, Any]]) -> str:
        """Handle question generation state"""
        # This state is typically handled automatically
        return self._generate_technical_questions()

    def _generate_technical_questions(self) -> str:
        """Generate technical questions based on collected data"""

        try:
            # Get candidate data
            candidate_data = self.context.collected_data
            tech_stack = candidate_data.get("tech_stack", "general programming")
            experience_years = candidate_data.get("experience_years", 1)
            name = candidate_data.get("name", "")

            # Generate questions using LLM service
            questions = llm_service.generate_technical_questions(
                tech_stack=tech_stack,
                experience_years=experience_years,
                candidate_name=name
            )

            if questions:
                # Store questions in context
                self.context.update_collected_data("technical_questions", questions)
                self.context.update_collected_data("current_question_index", 0)
                self.context.transition_to(ConversationState.AWAITING_TECH_ANSWERS)

                # Return introduction and first question
                intro = TechnicalQuestionPrompts.get_question_introduction(name, len(questions))
                first_question = TechnicalQuestionPrompts.get_question_prompt_template(
                    questions[0], 1, len(questions)
                )

                return f"{intro}\n\n{first_question}"
            else:
                # Fallback if question generation fails
                self.context.transition_to(ConversationState.COMPLETED)
                return "I apologize, but I'm having trouble generating technical questions right now. Let's complete your profile for now."

        except Exception as e:
            log_error(logger, e, self.session_id, {"action": "generate_technical_questions"})
            self.context.transition_to(ConversationState.ERROR)
            return FallbackPrompts.get_error_message("api_error")

    def _handle_tech_answers(self, user_input: str, conversation_history: List[Dict[str, Any]]) -> str:
        """Handle technical question answers"""

        try:
            # Get current question info
            questions = self.context.collected_data.get("technical_questions", [])
            current_index = self.context.collected_data.get("current_question_index", 0)

            if not questions or current_index >= len(questions):
                # No more questions - complete interview
                self.context.transition_to(ConversationState.COMPLETED)
                return self._handle_completion()

            # Store the answer
            current_question = questions[current_index]
            responses = self.context.collected_data.get("responses", [])
            responses.append({
                "question": current_question["question"],
                "answer": user_input,
                "question_index": current_index,
                "timestamp": datetime.now().isoformat()
            })

            self.context.update_collected_data("responses", responses)

            # Move to next question
            next_index = current_index + 1
            self.context.update_collected_data("current_question_index", next_index)

            if next_index < len(questions):
                # More questions available
                next_question = questions[next_index]
                question_prompt = TechnicalQuestionPrompts.get_question_prompt_template(
                    next_question, next_index + 1, len(questions)
                )

                encouragement = FallbackPrompts.get_encouragement()
                return f"{encouragement}\n\n{question_prompt}"
            else:
                # All questions completed
                self.context.transition_to(ConversationState.COMPLETED)
                return self._handle_completion()

        except Exception as e:
            log_error(logger, e, self.session_id, {"action": "handle_tech_answers"})
            return FallbackPrompts.get_error_message("general")

    def _handle_completion(self) -> str:
        """Handle interview completion"""
        name = self.context.collected_data.get("name", "there")
        return GreetingPrompts.get_completion_message(name)

    def _handle_completed_state(self, user_input: str, conversation_history: List[Dict[str, Any]]) -> str:
        """Handle completed state"""
        return "Your screening process is already complete! Thank you for your time with TalentScout."

    def _handle_error_state(self, user_input: str, conversation_history: List[Dict[str, Any]]) -> str:
        """Handle error state"""
        # Try to recover by resetting to appropriate state
        if self.context.is_data_complete(self.required_fields):
            self.context.transition_to(ConversationState.COMPLETED)
            return self._handle_completion()
        else:
            # Find the next field to collect
            next_field = self._find_next_field_to_collect()
            if next_field:
                state_map = {
                    "name": ConversationState.COLLECTING_NAME,
                    "email": ConversationState.COLLECTING_EMAIL,
                    "phone": ConversationState.COLLECTING_PHONE,
                    "experience_years": ConversationState.COLLECTING_EXPERIENCE,
                    "tech_stack": ConversationState.COLLECTING_TECH_STACK
                }

                new_state = state_map.get(next_field, ConversationState.GREETING)
                self.context.transition_to(new_state)
                return f"Let's continue from where we left off. {self._get_field_prompt(next_field)}"
            else:
                self.context.transition_to(ConversationState.GREETING)
                return GreetingPrompts.WELCOME_MESSAGE

    def _handle_exit(self) -> str:
        """Handle user exit"""
        return FallbackPrompts.get_end_conversation_prompts()["user_exit"]

    def _find_next_field_to_collect(self) -> Optional[str]:
        """Find the next field that needs to be collected"""
        for field in self.required_fields:
            if not self.context.collected_data.get(field):
                return field
        return None

    def _get_field_prompt(self, field: str) -> str:
        """Get prompt for specific field"""
        prompts = {
            "name": InfoCollectionPrompts.get_name_prompt(),
            "email": InfoCollectionPrompts.get_email_prompt(),
            "phone": InfoCollectionPrompts.get_phone_prompt(),
            "experience_years": InfoCollectionPrompts.get_experience_prompt(),
            "tech_stack": InfoCollectionPrompts.get_tech_stack_prompt()
        }
        return prompts.get(field, "Please provide the requested information.")

    def _get_context_dict(self) -> Dict[str, Any]:
        """Get context as dictionary"""
        return {
            "current_state": self.context.current_state.value,
            "previous_state": self.context.previous_state.value if self.context.previous_state else None,
            "retry_count": self.context.retry_count,
            "awaiting_field": self.context.awaiting_field,
            "collected_data": self.context.collected_data,
            "validation_errors": self.context.validation_errors,
            "completion_percentage": self._calculate_completion_percentage()
        }

    def _calculate_completion_percentage(self) -> float:
        """Calculate completion percentage"""
        completed_fields = sum(1 for field in self.required_fields 
                             if self.context.collected_data.get(field))
        return (completed_fields / len(self.required_fields)) * 100

    def get_initial_message(self) -> str:
        """Get initial greeting message"""
        return GreetingPrompts.WELCOME_MESSAGE

    def reset_conversation(self) -> None:
        """Reset conversation to initial state"""
        self.context = ConversationContext()
        log_conversation_event(
            logger,
            "conversation_reset",
            self.session_id,
            self.context.current_state.value
        )
