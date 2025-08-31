"""
Evaluation service for checking LLM outputs for hallucinations and bias.
"""
from typing import List, Dict, Any
from utils.logger import logger


# Do not import llm_service at module import time to avoid circular import issues.
# The LLM service instance will be resolved lazily inside the EvaluationService.

class EvaluationService:
    """
    Service for evaluating LLM-generated content for quality, relevance, and bias.
    """

    def __init__(self):
        """
        Initializes the EvaluationService.
        """
        # Lazily import the LLM service to prevent circular import during module import
        try:
            from services.llm_service import llm_service
            self.llm_service = llm_service
        except Exception:
            # If import fails at module import time (e.g., during tests), set to None.
            self.llm_service = None

    def check_hallucination(self, questions: List[Dict[str, Any]], tech_stack: str, experience_years: int) -> List[Dict[str, Any]]:
        """
        Checks for hallucinated or irrelevant questions.
        """
        # Ensure llm_service is available (lazy import if needed)
        if self.llm_service is None:
            try:
                from services.llm_service import llm_service
                self.llm_service = llm_service
            except Exception:
                logger.warning("LLM service not available (import failed), skipping hallucination check.")
                return questions

        if not self.llm_service.is_available():
            logger.warning("LLM service not available, skipping hallucination check.")
            return questions

        try:
            system_prompt = """
            You are an expert in technical interviews and software development.
            Your task is to validate a list of technical questions based on a candidate's tech stack and experience.
            A question is a hallucination if it is not relevant to the provided tech stack or appropriate for the experience level.
            Filter out any questions that are irrelevant or not suitable.
            Return a JSON object with a key "validated_questions" containing the list of valid questions.
            """

            user_prompt = f"""
            Tech Stack: {tech_stack}
            Experience Years: {experience_years}
            Questions to validate:
            {questions}
            """

            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]

            response = self.llm_service.generate_response(messages=messages)
            validated_data = self.llm_service._parse_json_response(response)
            return validated_data.get("validated_questions", questions)

        except Exception as e:
            logger.error(f"Error during hallucination check: {e}")
            return questions

    def check_bias(self, questions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Checks for biased content in questions.
        """
        # Ensure llm_service is available (lazy import if needed)
        if self.llm_service is None:
            try:
                from services.llm_service import llm_service
                self.llm_service = llm_service
            except Exception:
                logger.warning("LLM service not available (import failed), skipping bias check.")
                return questions

        if not self.llm_service.is_available():
            logger.warning("LLM service not available, skipping bias check.")
            return questions

        try:
            system_prompt = """
            You are an expert in creating fair and unbiased interview questions.
            Your task is to review a list of technical questions and identify any that contain biased language or assumptions (e.g., related to gender, race, age, or culture).
            Filter out any questions that are not neutral.
            Return a JSON object with a key "validated_questions" containing the list of unbiased questions.
            """

            user_prompt = f"""
            Questions to validate:
            {questions}
            """

            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]

            response = self.llm_service.generate_response(messages=messages)
            validated_data = self.llm_service._parse_json_response(response)
            return validated_data.get("validated_questions", questions)

        except Exception as e:
            logger.error(f"Error during bias check: {e}")
            return questions

    def evaluate_questions(self, questions: List[Dict[str, Any]], tech_stack: str, experience_years: int) -> List[Dict[str, Any]]:
        """
        Runs the full evaluation pipeline on a list of questions.
        """
        logger.info(f"Starting evaluation for {len(questions)} questions.")
        
        # Step 1: Check for hallucinations and relevance
        questions = self.check_hallucination(questions, tech_stack, experience_years)
        logger.info(f"{len(questions)} questions remaining after hallucination check.")

        # Step 2: Check for bias
        questions = self.check_bias(questions)
        logger.info(f"{len(questions)} questions remaining after bias check.")

        return questions

evaluation_service = EvaluationService()
