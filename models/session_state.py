"""
Session state management models
"""
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
from pydantic import BaseModel, Field

from utils.constants import ConversationState

class ConversationContext(BaseModel):
    """Context for conversation management"""
    current_state: ConversationState = Field(default=ConversationState.GREETING)
    previous_state: Optional[ConversationState] = Field(None)
    retry_count: int = Field(default=0)
    error_count: int = Field(default=0)
    awaiting_field: Optional[str] = Field(None)
    collected_data: Dict[str, Any] = Field(default_factory=dict)
    validation_errors: List[str] = Field(default_factory=list)

    def transition_to(self, new_state: ConversationState):
        """Transition to a new state"""
        self.previous_state = self.current_state
        self.current_state = new_state
        self.retry_count = 0  # Reset retry count on state change
        self.validation_errors.clear()  # Clear validation errors

    def increment_retry(self):
        """Increment retry count"""
        self.retry_count += 1

    def add_validation_error(self, error: str):
        """Add validation error"""
        self.validation_errors.append(error)

    def clear_validation_errors(self):
        """Clear validation errors"""
        self.validation_errors.clear()

    def set_awaiting_field(self, field: str):
        """Set the field we're currently collecting"""
        self.awaiting_field = field

    def update_collected_data(self, field: str, value: Any):
        """Update collected data"""
        self.collected_data[field] = value

    def is_data_complete(self, required_fields: List[str]) -> bool:
        """Check if all required data is collected"""
        return all(self.collected_data.get(field) for field in required_fields)

class StreamlitSessionState(BaseModel):
    """Model for Streamlit session state"""
    session_id: str = Field(..., description="Unique session identifier")
    initialized: bool = Field(default=False)
    messages: List[Dict[str, Any]] = Field(default_factory=list)
    conversation_context: ConversationContext = Field(default_factory=ConversationContext)
    user_data: Dict[str, Any] = Field(default_factory=dict)
    technical_questions: List[Dict[str, Any]] = Field(default_factory=list)
    current_question_index: int = Field(default=0)
    interview_completed: bool = Field(default=False)
    error_messages: List[str] = Field(default_factory=list)

    # Session management
    max_inactive_minutes: int = Field(default=30)
    last_interaction: datetime = Field(default_factory=datetime.now)

    def add_message(self, role: str, content: str):
        """Add a message to the conversation"""
        message = {
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        }
        self.messages.append(message)
        self.update_last_interaction()

    def update_last_interaction(self):
        """Update last interaction time"""
        self.last_interaction = datetime.now()

    def is_session_expired(self) -> bool:
        """Check if session has expired"""
        if not self.last_interaction:
            return True

        expiry_time = self.last_interaction + timedelta(minutes=self.max_inactive_minutes)
        return datetime.now() > expiry_time

    def get_conversation_duration(self) -> timedelta:
        """Get conversation duration"""
        if not self.messages:
            return timedelta(0)

        first_message_time = datetime.fromisoformat(self.messages[0]["timestamp"])
        return datetime.now() - first_message_time

    def clear_error_messages(self):
        """Clear error messages"""
        self.error_messages.clear()

    def add_error_message(self, error: str):
        """Add error message"""
        self.error_messages.append(error)

    def reset_conversation(self):
        """Reset conversation state"""
        self.messages.clear()
        self.conversation_context = ConversationContext()
        self.user_data.clear()
        self.technical_questions.clear()
        self.current_question_index = 0
        self.interview_completed = False
        self.error_messages.clear()
        self.update_last_interaction()

    class Config:
        arbitrary_types_allowed = True
