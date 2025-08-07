"""
LLM service for handling OpenRouter API interactions
"""
import json
import time
from typing import Dict, Any, List, Optional, Union
from openai import OpenAI
import streamlit as st

from config.settings import settings
from utils.logger import logger, log_error
from utils.helpers import generate_session_id

class LLMService:
    """Service for handling Language Model interactions via OpenRouter"""

    def __init__(self):
        """Initialize LLM service"""
        self.client = None
        self.session_id = generate_session_id()
        self._initialize_client()

    def _initialize_client(self) -> None:
        """Initialize OpenRouter client"""
        try:
            if not settings.validate_api_key():
                logger.warning("OpenRouter API key not configured")
                return

            self.client = OpenAI(
                base_url=settings.OPENROUTER_BASE_URL,
                api_key=settings.OPENROUTER_API_KEY,
                default_headers={
                    "HTTP-Referer": "https://talentscout-hiring-assistant.streamlit.app",
                    "X-Title": "TalentScout Hiring Assistant"
                }
            )
            logger.info("LLM service initialized successfully")

        except Exception as e:
            log_error(logger, e, self.session_id, {"action": "initialize_client"})
            self.client = None

    def is_available(self) -> bool:
        """Check if LLM service is available"""
        return self.client is not None and settings.validate_api_key()

    def generate_response(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None,
        stream: bool = False
    ) -> Union[str, Any]:
        """Generate response from LLM"""

        if not self.is_available():
            raise Exception("LLM service is not available. Please check API configuration.")

        try:
            model = model or settings.DEFAULT_MODEL
            max_tokens = max_tokens or settings.MAX_TOKENS
            temperature = temperature or settings.TEMPERATURE

            logger.info(
                "Generating LLM response",
                session_id=self.session_id,
                model=model,
                message_count=len(messages),
                stream=stream
            )

            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature,
                stream=stream
            )

            if stream:
                return response  # Return stream object for streaming responses
            else:
                content = response.choices[0].message.content
                logger.info("LLM response generated successfully", session_id=self.session_id)
                return content

        except Exception as e:
            log_error(logger, e, self.session_id, {
                "action": "generate_response",
                "model": model,
                "message_count": len(messages)
            })

            # Try fallback model if primary model fails
            if model != settings.FALLBACK_MODEL:
                logger.info("Trying fallback model", session_id=self.session_id)
                return self.generate_response(
                    messages, 
                    model=settings.FALLBACK_MODEL,
                    max_tokens=max_tokens,
                    temperature=temperature,
                    stream=stream
                )

            raise Exception(f"Failed to generate response: {str(e)}")

    def generate_technical_questions(
        self,
        tech_stack: str,
        experience_years: int,
        candidate_name: str = ""
    ) -> List[Dict[str, Any]]:
        """Generate technical questions based on candidate profile"""

        try:
            from prompts.tech_question_prompt import TechnicalQuestionPrompts

            # Create system message for question generation
            system_message = TechnicalQuestionPrompts.SYSTEM_PROMPT_FOR_QUESTION_GENERATION

            # Create user prompt with candidate details
            user_prompt = TechnicalQuestionPrompts.generate_question_prompt(
                tech_stack, experience_years, candidate_name
            )

            messages = [
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_prompt}
            ]

            # Generate questions
            response = self.generate_response(
                messages=messages,
                temperature=0.8  # Slightly higher temperature for creativity
            )

            # Parse JSON response
            try:
                questions_data = json.loads(response)
                questions = questions_data.get("questions", [])

                # Validate and clean questions
                validated_questions = []
                for q in questions:
                    if self._validate_question(q):
                        validated_questions.append(q)

                logger.info(
                    "Technical questions generated",
                    session_id=self.session_id,
                    question_count=len(validated_questions),
                    experience_years=experience_years
                )

                return validated_questions

            except json.JSONDecodeError:
                logger.warning("Failed to parse questions JSON, using fallback")
                return self._get_fallback_questions(experience_years)

        except Exception as e:
            log_error(logger, e, self.session_id, {
                "action": "generate_technical_questions",
                "tech_stack": tech_stack,
                "experience_years": experience_years
            })

            # Return fallback questions
            return self._get_fallback_questions(experience_years)

    def _validate_question(self, question: Dict[str, Any]) -> bool:
        """Validate question structure"""
        required_fields = ["question", "category", "difficulty"]
        return all(field in question and question[field] for field in required_fields)

    def _get_fallback_questions(self, experience_years: int) -> List[Dict[str, Any]]:
        """Get fallback questions when generation fails"""
        from prompts.tech_question_prompt import QuestionFallbacks
        return QuestionFallbacks.get_fallback_questions(experience_years)

    def validate_response(
        self,
        question: str,
        response: str,
        tech_context: str = ""
    ) -> Dict[str, Any]:
        """Validate and evaluate candidate response"""

        try:
            system_message = """You are an expert technical interviewer. Evaluate the candidate's response and provide brief feedback.

Rate the response on:
1. Technical accuracy (1-5)
2. Depth of knowledge (1-5)  
3. Clarity of explanation (1-5)
4. Practical experience shown (1-5)

Return evaluation in this JSON format:
{
  "overall_score": 4.2,
  "technical_accuracy": 4,
  "depth": 4,
  "clarity": 5,
  "practical_experience": 4,
  "feedback": "Brief feedback here",
  "strengths": ["strength1", "strength2"],
  "areas_for_improvement": ["area1", "area2"]
}"""

            user_prompt = f"""Question: {question}

Candidate Response: {response}

Technical Context: {tech_context}

Please evaluate this response."""

            messages = [
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_prompt}
            ]

            evaluation = self.generate_response(messages=messages, temperature=0.3)

            try:
                return json.loads(evaluation)
            except json.JSONDecodeError:
                return {
                    "overall_score": 3.0,
                    "feedback": "Response received and recorded.",
                    "technical_accuracy": 3,
                    "depth": 3,
                    "clarity": 3,
                    "practical_experience": 3
                }

        except Exception as e:
            log_error(logger, e, self.session_id, {"action": "validate_response"})
            return {
                "overall_score": 3.0,
                "feedback": "Response received and recorded.",
                "error": str(e)
            }

    def generate_conversation_response(
        self,
        user_input: str,
        conversation_history: List[Dict[str, str]],
        context: Dict[str, Any] = None
    ) -> str:
        """Generate contextual conversation response"""

        try:
            # Build conversation context
            messages = conversation_history.copy()

            # Add context if provided
            if context:
                context_info = f"Context: {json.dumps(context, default=str)}"
                messages.append({"role": "system", "content": context_info})

            # Add user input
            messages.append({"role": "user", "content": user_input})

            # Generate response
            response = self.generate_response(
                messages=messages,
                temperature=0.7
            )

            return response

        except Exception as e:
            log_error(logger, e, self.session_id, {"action": "generate_conversation_response"})
            return "I apologize, but I'm having trouble processing your request. Could you please try again?"

    def stream_response(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None
    ):
        """Generate streaming response"""

        if not self.is_available():
            yield "LLM service is not available. Please check API configuration."
            return

        try:
            response_stream = self.generate_response(
                messages=messages,
                model=model,
                stream=True
            )

            for chunk in response_stream:
                if chunk.choices[0].delta.content is not None:
                    yield chunk.choices[0].delta.content

        except Exception as e:
            log_error(logger, e, self.session_id, {"action": "stream_response"})
            yield f"Error generating response: {str(e)}"

    def health_check(self) -> Dict[str, Any]:
        """Perform health check on LLM service"""
        try:
            if not self.is_available():
                return {
                    "status": "unhealthy",
                    "error": "API key not configured or client not initialized"
                }

            # Simple test request
            test_messages = [
                {"role": "user", "content": "Hello, respond with 'OK' if you're working."}
            ]

            start_time = time.time()
            response = self.generate_response(test_messages, max_tokens=10)
            response_time = time.time() - start_time

            return {
                "status": "healthy" if response else "unhealthy",
                "response_time": round(response_time, 2),
                "model": settings.DEFAULT_MODEL,
                "test_response": response[:50] if response else None
            }

        except Exception as e:
            return {
                "status": "unhealthy",
                "error": str(e),
                "model": settings.DEFAULT_MODEL
            }

# Global LLM service instance
llm_service = LLMService()
