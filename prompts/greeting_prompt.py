"""
Greeting prompts for TalentScout Hiring Assistant
"""
from typing import Dict, Any

class GreetingPrompts:
    """Collection of greeting and introduction prompts"""

    SYSTEM_GREETING = """You are an AI hiring assistant for TalentScout, a leading recruitment agency specializing in technology placements. Your role is to conduct initial candidate screenings in a professional, friendly, and engaging manner.

Your objectives:
1. Welcome candidates warmly and explain your purpose
2. Collect essential candidate information systematically
3. Generate relevant technical questions based on their tech stack
4. Maintain a conversational and supportive tone throughout
5. Handle any errors or confusion gracefully

Guidelines:
- Be professional but approachable
- Ask one question at a time
- Provide clear instructions
- Acknowledge responses positively
- If you don't understand something, ask for clarification politely
- Keep responses concise but informative

Remember: You're representing TalentScout and creating the first impression for potential candidates."""

    WELCOME_MESSAGE = """🌟 Welcome to TalentScout! 🌟

Hello! I'm your AI hiring assistant, and I'm excited to help you get started with our screening process. TalentScout is a leading recruitment agency that specializes in connecting talented tech professionals with innovative companies.

I'm here to:
✅ Learn about your background and experience
✅ Understand your technical expertise
✅ Ask you some relevant questions about your skills
✅ Help match you with the right opportunities

This process typically takes 10-15 minutes, and all your information will be kept confidential and used only for recruitment purposes.

Ready to get started? Let's begin with some basic information about you! 🚀

**What's your full name?**"""

    COMPANY_INTRODUCTION = """Let me tell you a bit about TalentScout:

🏢 **About Us**: We're a leading recruitment agency specializing in technology placements
🎯 **Our Mission**: Connecting talented individuals with innovative companies
🤝 **Our Approach**: We focus on understanding both technical skills and cultural fit
🌍 **Our Reach**: We work with startups, scale-ups, and established tech companies

We believe that the right match benefits both candidates and companies, which is why we take time to understand your skills and career goals."""

    @staticmethod
    def get_state_transition_message(current_state: str, next_state: str) -> str:
        """Get appropriate transition message between states"""
        transitions = {
            ("greeting", "collecting_name"): "Great! Let's start by getting to know you better.",
            ("collecting_name", "collecting_email"): "Nice to meet you! Now I need your contact information.",
            ("collecting_email", "collecting_phone"): "Perfect! I also need your phone number.",
            ("collecting_phone", "collecting_experience"): "Excellent! Now let's talk about your experience.",
            ("collecting_experience", "collecting_tech_stack"): "Great! Now tell me about your technical expertise.",
            ("collecting_tech_stack", "generating_questions"): "Wonderful! Let me prepare some technical questions for you.",
            ("generating_questions", "awaiting_tech_answers"): "Here are some questions to assess your technical knowledge:",
            ("awaiting_tech_answers", "completed"): "Thank you for your responses! You've completed the screening process."
        }

        return transitions.get((current_state, next_state), "Let's continue with the next step.")

    @staticmethod
    def get_encouragement_message() -> str:
        """Get a random encouragement message"""
        messages = [
            "You're doing great! 👍",
            "Excellent! Let's keep going. 🚀",
            "Perfect! Thanks for the information. ✨",
            "Great job! Moving along nicely. 💫",
            "Wonderful! Almost there. 🌟"
        ]
        import random
        return random.choice(messages)

    @staticmethod
    def get_error_recovery_message(error_type: str = "general") -> str:
        """Get error recovery message based on error type"""
        messages = {
            "validation": "I notice there might be an issue with the format. Let me help you with that.",
            "timeout": "It seems like our conversation was interrupted. No worries, let's continue from where we left off.",
            "general": "I apologize for any confusion. Let me try to help you in a different way.",
            "network": "It looks like there was a connection issue. Let's try that again.",
            "retry": "Let's try that one more time. I want to make sure I get your information correctly."
        }

        return messages.get(error_type, messages["general"])

    @staticmethod
    def get_completion_message(candidate_name: str = "there") -> str:
        """Get completion message"""
        return f"""🎉 **Congratulations {candidate_name}!** 🎉

You've successfully completed the TalentScout screening process! Here's what happens next:

✅ **Your Information**: All your responses have been securely recorded
📋 **Review Process**: Our recruitment team will review your profile
🤝 **Next Steps**: If there's a good match, we'll contact you within 48-72 hours
📧 **Stay Connected**: Keep an eye on your email for updates

**Thank you for your time and interest in working with TalentScout!**

We're excited about the possibility of helping you find your next great opportunity. Your technical skills and experience will be valuable to the right company.

If you have any questions, feel free to reach out to our team. Good luck! 🍀"""

    @staticmethod
    def customize_greeting(candidate_data: Dict[str, Any] = None) -> str:
        """Customize greeting based on candidate data"""
        if not candidate_data:
            return GreetingPrompts.WELCOME_MESSAGE

        name = candidate_data.get("name", "")
        if name:
            return f"""Hello {name}! 👋

Welcome back to TalentScout! I see we were in the middle of collecting your information. Let's continue where we left off to complete your screening process.

Don't worry - I've saved all the information you've already provided, so we can pick up right from where we stopped.

Ready to continue? 🚀"""

        return GreetingPrompts.WELCOME_MESSAGE
