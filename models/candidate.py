"""
Pydantic models for candidate data validation
"""
from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field, validator
from enum import Enum

class ExperienceLevel(str, Enum):
    """Experience level enumeration"""
    JUNIOR = "junior"
    MID = "mid"
    SENIOR = "senior"

class InterviewStatus(str, Enum):
    """Interview status enumeration"""
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class CandidateInfo(BaseModel):
    """Model for candidate basic information"""
    name: str = Field(..., min_length=2, max_length=100, description="Candidate's full name")
    email: EmailStr = Field(..., description="Candidate's email address")
    phone: str = Field(..., min_length=10, max_length=20, description="Candidate's phone number")
    experience_years: int = Field(..., ge=0, le=50, description="Years of experience")
    tech_stack: str = Field(..., min_length=3, description="Technologies and skills")

    @validator('name')
    def validate_name(cls, v):
        if not v.strip():
            raise ValueError('Name cannot be empty')
        # Remove extra spaces
        return ' '.join(v.strip().split())

    @validator('phone')
    def validate_phone(cls, v):
        # Remove common phone number characters
        import re
        cleaned = re.sub(r'[\s\-\(\)\.]', '', v)
        if not re.match(r'^[\+]?[1-9][\d]{9,15}$', cleaned):
            raise ValueError('Invalid phone number format')
        return cleaned

    @validator('tech_stack')
    def validate_tech_stack(cls, v):
        if not v.strip():
            raise ValueError('Tech stack cannot be empty')
        return v.strip()

class TechnicalQuestion(BaseModel):
    """Model for technical questions"""
    question: str = Field(..., description="The technical question")
    category: str = Field(..., description="Question category (e.g., frontend, backend)")
    difficulty: str = Field(default="medium", description="Question difficulty level")
    expected_topics: List[str] = Field(default_factory=list, description="Expected topics in answer")

class CandidateResponse(BaseModel):
    """Model for candidate responses to technical questions"""
    question_id: str = Field(..., description="Unique identifier for the question")
    question: str = Field(..., description="The question that was asked")
    response: str = Field(..., description="Candidate's response")
    timestamp: datetime = Field(default_factory=datetime.now, description="Response timestamp")

    @validator('response')
    def validate_response(cls, v):
        if not v.strip():
            raise ValueError('Response cannot be empty')
        return v.strip()

class SessionData(BaseModel):
    """Model for session data"""
    session_id: str = Field(..., description="Unique session identifier")
    created_at: datetime = Field(default_factory=datetime.now, description="Session creation time")
    last_activity: datetime = Field(default_factory=datetime.now, description="Last activity time")
    current_state: str = Field(default="greeting", description="Current conversation state")
    candidate_info: Optional[CandidateInfo] = Field(None, description="Candidate information")
    technical_questions: List[TechnicalQuestion] = Field(default_factory=list, description="Generated technical questions")
    responses: List[CandidateResponse] = Field(default_factory=list, description="Candidate responses")
    conversation_history: List[Dict[str, Any]] = Field(default_factory=list, description="Full conversation history")
    is_active: bool = Field(default=True, description="Whether session is active")
    completion_percentage: float = Field(default=0.0, ge=0, le=100, description="Completion percentage")

    def update_last_activity(self):
        """Update last activity timestamp"""
        self.last_activity = datetime.now()

    def add_message(self, role: str, content: str):
        """Add message to conversation history"""
        self.conversation_history.append({
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        })
        self.update_last_activity()

    def get_collected_fields(self) -> Dict[str, Any]:
        """Get currently collected candidate fields"""
        if not self.candidate_info:
            return {}

        return {
            "name": getattr(self.candidate_info, 'name', None),
            "email": getattr(self.candidate_info, 'email', None),
            "phone": getattr(self.candidate_info, 'phone', None),
            "experience_years": getattr(self.candidate_info, 'experience_years', None),
            "tech_stack": getattr(self.candidate_info, 'tech_stack', None)
        }

class InterviewSummary(BaseModel):
    """Model for interview summary"""
    session_id: str = Field(..., description="Session identifier")
    candidate_info: CandidateInfo = Field(..., description="Candidate information")
    interview_date: datetime = Field(default_factory=datetime.now, description="Interview date")
    duration_minutes: Optional[int] = Field(None, description="Interview duration in minutes")
    status: InterviewStatus = Field(default=InterviewStatus.IN_PROGRESS, description="Interview status")
    technical_questions_count: int = Field(default=0, description="Number of technical questions asked")
    responses_count: int = Field(default=0, description="Number of responses received")
    completion_percentage: float = Field(default=0.0, description="Interview completion percentage")
    notes: Optional[str] = Field(None, description="Additional notes")

    class Config:
        use_enum_values = True

class CandidateDatabase(BaseModel):
    """Model for the candidate database"""
    candidates: List[InterviewSummary] = Field(default_factory=list, description="List of candidates")
    last_updated: datetime = Field(default_factory=datetime.now, description="Last update timestamp")
    total_candidates: int = Field(default=0, description="Total number of candidates")

    def add_candidate(self, summary: InterviewSummary):
        """Add a candidate to the database"""
        self.candidates.append(summary)
        self.total_candidates = len(self.candidates)
        self.last_updated = datetime.now()

    def get_candidate_by_email(self, email: str) -> Optional[InterviewSummary]:
        """Get candidate by email"""
        for candidate in self.candidates:
            if candidate.candidate_info.email == email:
                return candidate
        return None

    def get_candidates_by_tech_stack(self, tech: str) -> List[InterviewSummary]:
        """Get candidates by technology"""
        matching_candidates = []
        for candidate in self.candidates:
            if tech.lower() in candidate.candidate_info.tech_stack.lower():
                matching_candidates.append(candidate)
        return matching_candidates
