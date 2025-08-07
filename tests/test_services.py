"""
Tests for services
"""
import pytest
from unittest.mock import Mock, patch

from services.conversation_service import ConversationService
from services.storage_service import StorageService
from utils.constants import ConversationState

def test_conversation_service_initialization():
    """Test conversation service initialization"""
    service = ConversationService("test-session")
    assert service.session_id == "test-session"
    assert service.context.current_state == ConversationState.GREETING

def test_conversation_service_name_validation():
    """Test name validation in conversation service"""
    service = ConversationService("test-session")

    # Valid name
    response, context = service.process_user_input("John Smith")
    assert "email" in response.lower()  # Should ask for email next
    assert context["collected_data"].get("name") == "John Smith"

def test_conversation_service_email_validation():
    """Test email validation"""
    service = ConversationService("test-session")
    service.context.current_state = ConversationState.COLLECTING_EMAIL

    # Invalid email
    response, context = service.process_user_input("invalid-email")
    assert "valid email" in response.lower()
    assert not context["collected_data"].get("email")

    # Valid email
    response, context = service.process_user_input("test@example.com")
    assert context["collected_data"].get("email") == "test@example.com"

def test_conversation_service_experience_validation():
    """Test experience validation"""
    service = ConversationService("test-session")
    service.context.current_state = ConversationState.COLLECTING_EXPERIENCE

    # Valid experience
    response, context = service.process_user_input("5 years")
    assert context["collected_data"].get("experience_years") == 5

    # Invalid experience
    response, context = service.process_user_input("not a number")
    assert not context["collected_data"].get("experience_years")

def test_storage_service_initialization():
    """Test storage service initialization"""
    service = StorageService()
    assert service.data_dir.exists()

@patch('services.storage_service.Path.exists')
@patch('builtins.open')
def test_storage_service_save_candidate(mock_open, mock_exists):
    """Test saving candidate data"""
    mock_exists.return_value = False
    mock_file = Mock()
    mock_open.return_value.__enter__.return_value = mock_file

    service = StorageService()

    candidate_data = {
        "name": "John Smith",
        "email": "john@example.com",
        "phone": "555-123-4567",
        "experience_years": 5,
        "tech_stack": "Python, Django",
        "technical_questions": [],
        "responses": []
    }

    result = service.save_candidate_data(candidate_data, "test-session")
    assert result == True  # Should succeed

def test_database_stats():
    """Test database statistics calculation"""
    service = StorageService()
    stats = service.get_database_stats()

    assert "total_candidates" in stats
    assert "completed_interviews" in stats
    assert "average_completion" in stats
    assert "experience_distribution" in stats
