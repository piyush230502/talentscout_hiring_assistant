"""
Fallback prompts for handling errors and edge cases
"""
from typing import List, Dict, Any
import random

class FallbackPrompts:
    """Collection of fallback prompts for error handling"""

    # General fallback responses
    GENERAL_FALLBACKS = [
        "I'm sorry, I didn't quite understand that. Could you please rephrase your response?",
        "Let me clarify - could you provide more details about that?",
        "I want to make sure I capture your information correctly. Could you elaborate?",
        "That's interesting! Could you give me a bit more context?",
        "I'd like to understand better. Could you explain that differently?"
    ]

    # Context-specific fallbacks
    CONTEXT_FALLBACKS = {
        "name_collection": [
            "I need to get your name correctly. Could you please tell me your full name?",
            "Let me make sure I have your name right. What should I call you?",
            "Could you please provide your first and last name?"
        ],
        "email_collection": [
            "I need a valid email address to contact you. Could you try again?",
            "Please provide your email address in the format: name@domain.com",
            "Let's try the email address once more - make sure it includes @ and a domain."
        ],
        "phone_collection": [
            "I need your phone number to reach you. Could you provide it again?",  
            "Please enter your phone number - any standard format is fine.",
            "Let me get your contact number. What's your phone number?"
        ],
        "experience_collection": [
            "I need to know your experience level. How many years have you worked in tech?",
            "Please tell me your years of experience as a number (like 3, 5, or 10).",
            "Could you provide your experience in years? New to tech? Just say 0 or 1."
        ],
        "tech_stack_collection": [
            "I need to understand your technical background. What technologies do you work with?",
            "Please tell me about your programming languages, frameworks, and tools.",
            "Could you list your technical skills and areas of expertise?"
        ]
    }

    # Error-specific messages
    ERROR_MESSAGES = {
        "validation_error": "I notice there might be an issue with the format. Let me help you with that.",
        "api_error": "I'm experiencing some technical difficulties. Let me try that again.",
        "timeout_error": "It seems like our connection was interrupted. Let's continue from where we left off.",
        "parsing_error": "I had trouble processing that response. Could you try rephrasing it?",
        "network_error": "There seems to be a connection issue. Let's try again.",
        "rate_limit": "I need to slow down a bit. Let's continue in just a moment.",
        "session_expired": "Our session timed out, but don't worry - let's start fresh!"
    }

    # Encouragement messages
    ENCOURAGEMENT_MESSAGES = [
        "You're doing great! Let's keep going. 👍",  
        "Perfect! Thanks for the information. ✨",
        "Excellent! Moving along nicely. 🚀",
        "Great job! Almost there. 💫",
        "Wonderful! This is going smoothly. 🌟"
    ]

    # Retry messages
    RETRY_MESSAGES = {
        1: "Let's try that once more.",
        2: "One more time - I want to make sure I get this right.",
        3: "Let me help you with this. Here's what I need:",
        4: "I'm having trouble with that format. Let me give you an example:",
        5: "This seems to be challenging. Would you like me to skip this for now?"
    }

    @staticmethod
    def get_fallback_response(context: str = "general", retry_count: int = 0) -> str:
        """Get appropriate fallback response based on context and retry count"""

        # If too many retries, suggest skipping or getting help
        if retry_count >= 5:
            return """I'm having trouble with this field. Would you like to:
1. Skip this for now and come back to it
2. Try a different format
3. Get help from our team

Just let me know how you'd like to proceed!"""

        # Get context-specific fallback if available
        if context in FallbackPrompts.CONTEXT_FALLBACKS:
            fallbacks = FallbackPrompts.CONTEXT_FALLBACKS[context]
            if fallbacks:
                return random.choice(fallbacks)

        # Get retry-specific message
        if retry_count in FallbackPrompts.RETRY_MESSAGES:
            return FallbackPrompts.RETRY_MESSAGES[retry_count]

        # Default to general fallback
        return random.choice(FallbackPrompts.GENERAL_FALLBACKS)

    @staticmethod
    def get_error_message(error_type: str) -> str:
        """Get error message for specific error type"""
        return FallbackPrompts.ERROR_MESSAGES.get(
            error_type, 
            "I apologize, but I encountered an issue. Let me try to help you in a different way."
        )

    @staticmethod
    def get_encouragement() -> str:
        """Get random encouragement message"""
        return random.choice(FallbackPrompts.ENCOURAGEMENT_MESSAGES)

    @staticmethod
    def get_clarification_prompt(field: str, provided_value: str) -> str:
        """Get clarification prompt for unclear input"""
        clarifications = {
            "name": f"I received '{provided_value}' as your name. Is this correct, or would you like to provide your full name?",
            "email": f"I received '{provided_value}' as your email. This doesn't look like a valid email format. Could you try again?",
            "phone": f"I received '{provided_value}' as your phone number. Could you confirm this is correct?",
            "experience": f"I received '{provided_value}' for your experience. Could you provide this as a number of years?",
            "tech_stack": f"I received '{provided_value}' as your tech stack. Could you provide more details about your technical skills?"
        }

        return clarifications.get(field, f"I received '{provided_value}'. Could you please clarify this?")

    @staticmethod
    def get_validation_help(field: str) -> str:
        """Get help message for field validation"""
        help_messages = {
            "name": """**Name Help:**
- Use your professional first and last name
- Example: "John Smith" or "Maria Rodriguez"
- Avoid nicknames or abbreviations""",

            "email": """**Email Help:**
- Must include @ symbol and domain
- Example: john.smith@email.com
- Use an email you check regularly""",

            "phone": """**Phone Help:**
- Include country code if outside US: +1-555-123-4567
- US format: 555-123-4567 or (555) 123-4567
- International: +44-20-1234-5678""",

            "experience": """**Experience Help:**
- Enter number of years only: 3, 5, 10
- Count internships and significant projects
- New to tech? Enter 0 or 1""",

            "tech_stack": """**Technical Skills Help:**
- List programming languages: Python, JavaScript, Java
- Include frameworks: React, Django, Spring
- Add databases: MySQL, MongoDB, PostgreSQL
- Mention cloud: AWS, Azure, Google Cloud"""
        }

        return help_messages.get(field, f"Please provide a valid {field}.")

    @staticmethod
    def get_skip_option_prompt(field: str) -> str:
        """Get prompt offering to skip a problematic field"""
        return f"""I'm having trouble collecting your {field}. Would you like to:

1. **Try again** - I'll help you with the format
2. **Skip for now** - We can come back to this later  
3. **Get help** - Connect with our team for assistance

What would you prefer? Just type 1, 2, or 3."""

    @staticmethod
    def get_session_recovery_prompt(partial_data: Dict[str, Any]) -> str:
        """Get prompt for recovering from session issues"""
        collected_fields = [k for k, v in partial_data.items() if v]

        if not collected_fields:
            return """It looks like we're starting fresh! No problem at all.

Let's begin with collecting your information for the TalentScout screening process."""

        fields_text = ", ".join(collected_fields)
        return f"""I see we were interrupted, but I've saved the information you already provided: {fields_text}.

Let's continue from where we left off. This helps us avoid having to start over completely!"""

    @staticmethod
    def get_technical_difficulty_prompt() -> str:
        """Get prompt when facing technical difficulties"""
        return """🔧 **Technical Difficulty**

I'm experiencing some technical issues, but don't worry! Here are your options:

1. **Wait a moment** - I'll try to resolve this automatically
2. **Refresh and continue** - Your progress is saved
3. **Contact support** - Our team can help you complete the process

Your information is secure and we'll make sure you can complete the screening process smoothly."""

    @staticmethod
    def get_end_conversation_prompts() -> Dict[str, str]:
        """Get prompts for ending conversation in different scenarios"""
        return {
            "user_exit": """Thank you for your time with TalentScout! 

If you'd like to complete the screening process later, just return to this page - I'll remember where we left off.

Have a great day! 🌟""",

            "timeout": """⏰ **Session Timeout**

Our conversation has been inactive for a while. For security reasons, I'll need to end this session.

Don't worry - if you provided any information, it's been saved. You can start a new session anytime to continue or complete the screening process.

Thank you for your interest in TalentScout! 🙏""",

            "error_exit": """I apologize, but I'm experiencing technical difficulties that prevent me from continuing.

**What to do next:**
✅ Your information is safely stored
✅ You can try again in a few minutes  
✅ Contact our team if the issue persists

Thank you for your patience! 🛠️""",

            "completion": """🎉 **Screening Complete!**

Congratulations! You've successfully completed the TalentScout screening process.

**Next Steps:**
✅ Your profile will be reviewed by our team
✅ We'll contact you within 48-72 hours if there's a match
✅ Keep an eye on your email for updates

Thank you for your time and interest in working with TalentScout! 🚀"""
        }
