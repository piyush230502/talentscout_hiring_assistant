"""
Information collection prompts for TalentScout Hiring Assistant
"""
from typing import Dict, Any, List

class InfoCollectionPrompts:
    """Collection of prompts for gathering candidate information"""

    @staticmethod
    def get_name_prompt(retry_count: int = 0) -> str:
        """Get prompt for collecting candidate name"""
        if retry_count == 0:
            return """**What's your full name?**

Please provide your first and last name as you'd like it to appear professionally."""

        elif retry_count == 1:
            return """I want to make sure I get your name right. 

**Could you please provide your full name?** 

(For example: "John Smith" or "Maria Garcia")"""

        else:
            return """Let me try once more. 

**Please enter your full name** - just your first and last name is perfect!"""

    @staticmethod
    def get_email_prompt(retry_count: int = 0, name: str = "") -> str:
        """Get prompt for collecting email address"""
        greeting = f"Thanks {name}! " if name else "Great! "

        if retry_count == 0:
            return f"""{greeting}**What's your email address?**

This will be our primary way to contact you about opportunities."""

        elif retry_count == 1:
            return """I need a valid email address to contact you.

**Please provide your email address** (for example: john.smith@email.com)"""

        else:
            return """Let's try the email address one more time.

**Please enter a valid email address** - make sure it includes @ and a domain (like .com, .org, etc.)"""

    @staticmethod
    def get_phone_prompt(retry_count: int = 0) -> str:
        """Get prompt for collecting phone number"""
        if retry_count == 0:
            return """Perfect! **What's your phone number?**

Please include your country code if you're outside the US (for example: +1-555-123-4567 or just 555-123-4567)"""

        elif retry_count == 1:
            return """I need a valid phone number to reach you.

**Please provide your phone number** - you can include or exclude dashes, spaces, and parentheses."""

        else:
            return """Let's get your phone number. 

**Please enter your phone number** - any standard format is fine (like 555-123-4567 or +1 555 123 4567)"""

    @staticmethod
    def get_experience_prompt(retry_count: int = 0) -> str:
        """Get prompt for collecting years of experience"""
        if retry_count == 0:
            return """Excellent! Now let's talk about your background.

**How many years of professional experience do you have in technology?**

Please provide a number (for example: 3, 5, or 10). Include internships and significant project work if you're early in your career."""

        elif retry_count == 1:
            return """I need to know your experience level to ask appropriate questions.

**How many years of tech experience do you have?** 

Just enter a number - if you're new to tech, you can enter 0 or 1."""

        else:
            return """Let's get your experience level.

**Please enter the number of years** you've been working in technology (0-50)"""

    @staticmethod
    def get_tech_stack_prompt(retry_count: int = 0, experience_years: int = 0) -> str:
        """Get prompt for collecting tech stack information"""
        experience_context = ""
        if experience_years == 0:
            experience_context = " Don't worry if you're just starting out - include any technologies you've learned or worked with during studies, bootcamps, or personal projects."
        elif experience_years <= 2:
            experience_context = " Include technologies from work, personal projects, and your learning journey."
        else:
            experience_context = " Focus on technologies you've used professionally and feel confident discussing."

        if retry_count == 0:
            return f"""Great! Now for the important part.

**What technologies, programming languages, frameworks, or tools do you work with?**

Please list your technical skills and areas of expertise. For example:
• Programming languages (Python, JavaScript, Java, etc.)
• Frameworks (React, Django, Spring, etc.)  
• Databases (MySQL, MongoDB, PostgreSQL, etc.)
• Cloud platforms (AWS, Azure, Google Cloud, etc.)
• Other tools and technologies

{experience_context}"""

        elif retry_count == 1:
            return f"""I need to understand your technical background to generate relevant questions.

**Please tell me about your technical skills and experience.**

You can mention programming languages, frameworks, databases, tools, or any technology you've worked with.{experience_context}"""

        else:
            return """Let's get your technical background.

**Please list any technologies, programming languages, or tools you've used** - even if you're just learning them!"""

    @staticmethod
    def get_validation_error_message(field: str, error_type: str) -> str:
        """Get validation error message for specific field and error type"""
        messages = {
            "name": {
                "empty": "Name cannot be empty. Please provide your full name.",
                "invalid": "Please provide a valid name with only letters, spaces, hyphens, and apostrophes.",
                "too_short": "Name seems too short. Please provide your full name.",
                "too_long": "Name seems too long. Please provide a shorter version."
            },
            "email": {
                "empty": "Email cannot be empty. Please provide your email address.",
                "invalid": "Please provide a valid email address (e.g., name@example.com).",
                "format": "Email format is incorrect. Please include @ and a domain."
            },
            "phone": {
                "empty": "Phone number cannot be empty. Please provide your phone number.",
                "invalid": "Please provide a valid phone number (10-15 digits, optionally with country code).",
                "format": "Phone number format is incorrect. Please use only numbers, +, -, (, ), spaces, and dots."
            },
            "experience": {
                "empty": "Experience cannot be empty. Please provide the number of years.",
                "invalid": "Please provide a valid number of years (0-50).",
                "negative": "Experience cannot be negative. Please enter 0 or a positive number.",
                "too_high": "Experience seems too high. Please enter a realistic number of years (0-50)."
            },
            "tech_stack": {
                "empty": "Tech stack cannot be empty. Please tell me about your technical skills.",
                "too_short": "Please provide more details about your technical skills and experience."
            }
        }

        return messages.get(field, {}).get(error_type, f"Please provide a valid {field}.")

    @staticmethod
    def get_confirmation_message(field: str, value: Any) -> str:
        """Get confirmation message for collected data"""
        confirmations = {
            "name": f"✅ Name: {value}",
            "email": f"✅ Email: {value}",
            "phone": f"✅ Phone: {value}",
            "experience": f"✅ Experience: {value} year{'s' if value != 1 else ''}",
            "tech_stack": f"✅ Technical Skills: {value}"
        }

        return confirmations.get(field, f"✅ {field.title()}: {value}")

    @staticmethod
    def get_data_summary(candidate_data: Dict[str, Any]) -> str:
        """Get summary of collected candidate data"""
        name = candidate_data.get("name", "")
        email = candidate_data.get("email", "")
        phone = candidate_data.get("phone", "")
        experience = candidate_data.get("experience_years", 0)
        tech_stack = candidate_data.get("tech_stack", "")

        return f"""📋 **Here's the information I've collected:**

✅ **Name**: {name}
✅ **Email**: {email}
✅ **Phone**: {phone}
✅ **Experience**: {experience} year{'s' if experience != 1 else ''}
✅ **Technical Skills**: {tech_stack}

Does this look correct? If you need to update any information, just let me know! Otherwise, I'll prepare some technical questions based on your expertise."""

    @staticmethod
    def get_progress_indicator(current_step: int, total_steps: int = 5) -> str:
        """Get progress indicator"""
        progress_bar = "▓" * current_step + "░" * (total_steps - current_step)
        percentage = int((current_step / total_steps) * 100)

        return f"Progress: [{progress_bar}] {percentage}% ({current_step}/{total_steps})"

    @staticmethod
    def get_field_specific_help(field: str) -> str:
        """Get help message for specific field"""
        help_messages = {
            "name": "💡 **Tip**: Use your professional name as you'd want it to appear on documents.",
            "email": "💡 **Tip**: Use an email you check regularly - this is how we'll contact you about opportunities.",
            "phone": "💡 **Tip**: Include country code if outside US. Format doesn't matter - we'll clean it up!",
            "experience": "💡 **Tip**: Count internships and significant project work. New to tech? Just enter 0 or 1.",
            "tech_stack": "💡 **Tip**: Include everything you've worked with - languages, frameworks, databases, cloud services, tools, etc."
        }

        return help_messages.get(field, "")
