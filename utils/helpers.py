"""
Helper functions for TalentScout Hiring Assistant
"""
import re
import uuid
import hashlib
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta

from utils.constants import VALIDATION_PATTERNS, EXIT_KEYWORDS, TECH_STACK_CATEGORIES

def generate_session_id() -> str:
    """Generate a unique session ID"""
    return str(uuid.uuid4())

def hash_email(email: str) -> str:
    """Hash email for privacy (optional)"""
    return hashlib.sha256(email.encode()).hexdigest()

def validate_email(email: str) -> bool:
    """Validate email format"""
    if not email:
        return False
    return bool(re.match(VALIDATION_PATTERNS["email"], email))

def validate_phone(phone: str) -> bool:
    """Validate phone number format"""
    if not phone:
        return False
    # Remove spaces and common separators
    clean_phone = re.sub(r'[\s\-\(\)\.]', '', phone)
    return bool(re.match(VALIDATION_PATTERNS["phone"], clean_phone))

def validate_name(name: str) -> bool:
    """Validate name format"""
    if not name:
        return False
    return bool(re.match(VALIDATION_PATTERNS["name"], name))

def is_exit_keyword(text: str) -> bool:
    """Check if user wants to exit"""
    if not text:
        return False
    return text.lower().strip() in EXIT_KEYWORDS

def clean_text_input(text: str) -> str:
    """Clean and normalize text input"""
    if not text:
        return ""
    return text.strip()

def extract_tech_stack(tech_input: str) -> Dict[str, List[str]]:
    """Extract and categorize technologies from user input"""
    tech_input_lower = tech_input.lower()
    categorized_tech = {}

    for category, data in TECH_STACK_CATEGORIES.items():
        found_techs = []
        for tech in data["technologies"]:
            if tech.lower() in tech_input_lower:
                found_techs.append(tech)

        if found_techs:
            categorized_tech[category] = found_techs

    return categorized_tech

def determine_experience_level(years: int) -> str:
    """Determine experience level based on years"""
    if years <= 2:
        return "junior"
    elif years <= 5:
        return "mid"
    else:
        return "senior"

def format_tech_stack_display(tech_stack: Dict[str, List[str]]) -> str:
    """Format tech stack for display"""
    if not tech_stack:
        return "No specific technologies identified"

    formatted_parts = []
    for category, technologies in tech_stack.items():
        tech_list = ", ".join(technologies)
        formatted_parts.append(f"{category.title()}: {tech_list}")

    return " | ".join(formatted_parts)

def truncate_conversation_history(messages: List[Dict[str, Any]], max_length: int = 50) -> List[Dict[str, Any]]:
    """Truncate conversation history to prevent memory issues"""
    if len(messages) <= max_length:
        return messages

    # Keep the first message (system prompt) and the most recent messages
    return [messages[0]] + messages[-(max_length-1):]

def is_session_expired(last_activity: datetime, timeout_minutes: int = 60) -> bool:
    """Check if session has expired"""
    if not last_activity:
        return True

    expiry_time = last_activity + timedelta(minutes=timeout_minutes)
    return datetime.now() > expiry_time

def sanitize_filename(filename: str) -> str:
    """Sanitize filename for safe storage"""
    # Remove or replace invalid characters
    sanitized = re.sub(r'[<>:"/\|?*]', '_', filename)
    return sanitized.strip()

def extract_numbers_from_text(text: str) -> List[int]:
    """Extract numbers from text"""
    numbers = re.findall(r'\d+', text)
    return [int(num) for num in numbers]

def format_duration(seconds: int) -> str:
    """Format duration in a human-readable way"""
    if seconds < 60:
        return f"{seconds} seconds"
    elif seconds < 3600:
        minutes = seconds // 60
        return f"{minutes} minutes"
    else:
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        return f"{hours} hours {minutes} minutes"

def mask_sensitive_data(data: str, mask_char: str = "*", visible_chars: int = 3) -> str:
    """Mask sensitive data for logging"""
    if not data or len(data) <= visible_chars * 2:
        return mask_char * len(data) if data else ""

    return data[:visible_chars] + mask_char * (len(data) - visible_chars * 2) + data[-visible_chars:]

def calculate_completion_percentage(collected_fields: Dict[str, Any], required_fields: List[str]) -> float:
    """Calculate completion percentage of required fields"""
    if not required_fields:
        return 100.0

    completed_count = sum(1 for field in required_fields if collected_fields.get(field))
    return (completed_count / len(required_fields)) * 100
