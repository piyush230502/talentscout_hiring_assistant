"""
Tests for Pydantic models
"""
import pytest
from datetime import datetime
from pydantic import ValidationError

from models.candidate import CandidateInfo, TechnicalQuestion, CandidateResponse, SessionData

def test_candidate_info_valid():
    """Test valid candidate info creation"""
    candidate = CandidateInfo(
        name="John Smith",
        email="john.smith@email.com",
        phone="555-123-4567",
        experience_years=5,
        tech_stack="Python, Django, PostgreSQL, AWS"
    )

    assert candidate.name == "John Smith"
    assert candidate.email == "john.smith@email.com"
    assert candidate.experience_years == 5

def test_candidate_info_invalid_email():
    """Test invalid email validation"""
    with pytest.raises(ValidationError):
        CandidateInfo(
            name="John Smith",
            email="invalid_email",
            phone="555-123-4567",
            experience_years=5,
            tech_stack="Python"
        )

def test_candidate_info_invalid_experience():
    """Test invalid experience validation"""
    with pytest.raises(ValidationError):
        CandidateInfo(
            name="John Smith",
            email="john@email.com",
            phone="555-123-4567",
            experience_years=-1,  # Invalid negative experience
            tech_stack="Python"
        )

def test_technical_question():
    """Test technical question model"""
    question = TechnicalQuestion(
        question="What is the difference between list and tuple in Python?",
        category="python",
        difficulty="junior",
        expected_topics=["data structures", "mutability"]
    )

    assert "Python" in question.question
    assert question.category == "python"
    assert question.difficulty == "junior"

def test_candidate_response():
    """Test candidate response model"""
    response = CandidateResponse(
        question_id="q1",
        question="What is Python?",
        response="Python is a programming language"
    )

    assert response.question_id == "q1"
    assert len(response.response) > 0
    assert isinstance(response.timestamp, datetime)

def test_session_data():
    """Test session data model"""
    session = SessionData(
        session_id="test-session-123"
    )

    assert session.session_id == "test-session-123"
    assert session.is_active == True
    assert session.completion_percentage == 0.0

    # Test adding message
    session.add_message("user", "Hello")
    assert len(session.conversation_history) == 1
    assert session.conversation_history[0]["role"] == "user"
    assert session.conversation_history[0]["content"] == "Hello"
