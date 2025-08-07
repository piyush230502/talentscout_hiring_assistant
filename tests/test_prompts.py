"""
Tests for prompt generation
"""
import pytest
from prompts.greeting_prompt import GreetingPrompts
from prompts.info_prompt import InfoCollectionPrompts
from prompts.tech_question_prompt import TechnicalQuestionPrompts
from prompts.fallback_prompt import FallbackPrompts

def test_greeting_prompts():
    """Test greeting prompt generation"""
    welcome = GreetingPrompts.WELCOME_MESSAGE
    assert "TalentScout" in welcome
    assert "name" in welcome.lower()

def test_greeting_customization():
    """Test customized greetings"""
    candidate_data = {"name": "John"}
    custom_greeting = GreetingPrompts.customize_greeting(candidate_data)
    assert "John" in custom_greeting

def test_info_collection_prompts():
    """Test information collection prompts"""
    name_prompt = InfoCollectionPrompts.get_name_prompt()
    assert "name" in name_prompt.lower()

    email_prompt = InfoCollectionPrompts.get_email_prompt(name="John")
    assert "John" in email_prompt
    assert "email" in email_prompt.lower()

def test_validation_error_messages():
    """Test validation error messages"""
    error_msg = InfoCollectionPrompts.get_validation_error_message("email", "invalid")
    assert "valid email" in error_msg.lower()

    error_msg = InfoCollectionPrompts.get_validation_error_message("name", "empty")
    assert "empty" in error_msg.lower()

def test_tech_question_prompts():
    """Test technical question prompt generation"""
    prompt = TechnicalQuestionPrompts.generate_question_prompt(
        "Python, Django", 5, "John Smith"
    )
    assert "Python" in prompt
    assert "Django" in prompt
    assert "5 years" in prompt

def test_question_introduction():
    """Test question introduction"""
    intro = TechnicalQuestionPrompts.get_question_introduction("John", 3)
    assert "John" in intro
    assert "questions" in intro.lower()

def test_fallback_prompts():
    """Test fallback prompt generation"""
    fallback = FallbackPrompts.get_fallback_response("general")
    assert len(fallback) > 0

    error_msg = FallbackPrompts.get_error_message("api_error")
    assert "technical" in error_msg.lower() or "error" in error_msg.lower()

def test_encouragement_messages():
    """Test encouragement message generation"""
    encouragement = FallbackPrompts.get_encouragement()
    assert len(encouragement) > 0

def test_retry_messages():
    """Test retry message handling"""
    retry_msg = FallbackPrompts.get_fallback_response("name_collection", retry_count=1)
    assert len(retry_msg) > 0

    skip_msg = FallbackPrompts.get_skip_option_prompt("email")
    assert "skip" in skip_msg.lower()
    assert "email" in skip_msg.lower()

def test_tech_stack_categorization():
    """Test tech stack categorization"""
    categorized = TechnicalQuestionPrompts.categorize_tech_stack("Python Django React PostgreSQL")

    assert "backend" in categorized  # Python, Django
    assert "frontend" in categorized  # React
    assert "database" in categorized  # PostgreSQL
