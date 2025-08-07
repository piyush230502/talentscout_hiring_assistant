"""
Technical question generation prompts for TalentScout Hiring Assistant
"""
from typing import List, Dict, Any
from utils.constants import TECH_STACK_CATEGORIES, EXPERIENCE_LEVEL_QUESTIONS

class TechnicalQuestionPrompts:
    """Collection of prompts for generating technical questions"""

    SYSTEM_PROMPT_FOR_QUESTION_GENERATION = """You are an expert technical interviewer for TalentScout, a leading recruitment agency. Your task is to generate relevant, fair, and appropriate technical questions based on a candidate's experience level and tech stack.

Guidelines for question generation:
1. Match question difficulty to experience level (junior/mid/senior)
2. Focus on technologies the candidate actually mentioned
3. Create 3-5 questions that test different aspects of their knowledge
4. Include a mix of conceptual and practical questions
5. Avoid overly complex or trick questions
6. Make questions clear and specific
7. Consider real-world applications

Question types to include:
- Core concept understanding
- Best practices and methodologies  
- Problem-solving scenarios
- Architecture and design (for mid/senior)
- Experience-based questions

Return questions in this JSON format:
{
  "questions": [
    {
      "question": "Question text here",
      "category": "frontend/backend/database/etc",
      "difficulty": "junior/mid/senior",
      "expected_topics": ["topic1", "topic2"]
    }
  ]
}"""

    @staticmethod
    def generate_question_prompt(
        tech_stack: str, 
        experience_years: int, 
        candidate_name: str = ""
    ) -> str:
        """Generate prompt for technical question creation"""

        experience_level = "junior" if experience_years <= 2 else "mid" if experience_years <= 5 else "senior"

        return f"""Generate 3-5 technical interview questions for a candidate with the following profile:

**Candidate Profile:**
- Name: {candidate_name}
- Experience: {experience_years} years ({experience_level} level)
- Technical Stack: {tech_stack}

**Requirements:**
1. Questions should be appropriate for {experience_level} level ({experience_years} years experience)
2. Focus only on technologies mentioned in their tech stack
3. Include a variety of question types (conceptual, practical, scenario-based)
4. Make questions specific and actionable
5. Avoid generic questions that could apply to any technology

**Experience Level Guidelines:**
- Junior (0-2 years): Basic concepts, syntax, simple problem-solving
- Mid (3-5 years): Best practices, architecture basics, debugging, optimization
- Senior (6+ years): System design, leadership, complex problem-solving, architectural decisions

Please generate questions that will help assess their actual knowledge and experience with the technologies they mentioned."""

    @staticmethod
    def get_question_introduction(candidate_name: str = "", tech_count: int = 0) -> str:
        """Get introduction message before technical questions"""
        name_part = f"Thanks {candidate_name}! " if candidate_name else "Perfect! "

        return f"""{name_part}🎯 **Technical Assessment Time!**

Based on your technical background, I've prepared some questions to better understand your expertise. These questions are designed to:

✅ Assess your knowledge of the technologies you mentioned
✅ Understand your problem-solving approach  
✅ Gauge your experience level
✅ Help match you with appropriate opportunities

**Guidelines:**
• Take your time to think through each question
• Provide detailed answers when possible
• It's okay to mention if you haven't used something extensively
• Focus on your actual experience and knowledge

Ready? Let's dive into your technical expertise! 🚀"""

    @staticmethod
    def get_question_prompt_template(question_data: Dict[str, Any], question_number: int, total_questions: int) -> str:
        """Format individual question prompt"""
        question = question_data.get("question", "")
        category = question_data.get("category", "").title()
        difficulty = question_data.get("difficulty", "")

        return f"""**Question {question_number} of {total_questions}** | Category: {category} | Level: {difficulty.title()}

{question}

💡 **Please provide a detailed answer based on your experience and knowledge.**"""

    @staticmethod
    def get_question_followup_prompts() -> Dict[str, str]:
        """Get follow-up prompts for different scenarios"""
        return {
            "short_answer": "That's a good start! Could you elaborate a bit more on your experience with this?",
            "unclear_answer": "Thanks for your response! Could you clarify what you mean by that?",
            "no_experience": "No problem if you haven't used this extensively! Can you tell me about something similar you have worked with?",
            "good_answer": "Excellent answer! That shows good understanding.",
            "partial_answer": "Good start! Is there anything else you'd like to add about this topic?"
        }

    @staticmethod
    def categorize_tech_stack(tech_stack: str) -> Dict[str, List[str]]:
        """Categorize technologies from tech stack string"""
        tech_stack_lower = tech_stack.lower()
        categorized = {}

        for category, data in TECH_STACK_CATEGORIES.items():
            found_techs = []
            for tech in data["technologies"]:
                if tech.lower() in tech_stack_lower:
                    found_techs.append(tech)

            if found_techs:
                categorized[category] = found_techs

        return categorized

    @staticmethod
    def get_experience_based_questions(experience_years: int) -> List[str]:
        """Get experience-level appropriate questions"""
        if experience_years <= 2:
            return EXPERIENCE_LEVEL_QUESTIONS["junior"]
        elif experience_years <= 5:
            return EXPERIENCE_LEVEL_QUESTIONS["mid"]
        else:
            return EXPERIENCE_LEVEL_QUESTIONS["senior"]

    @staticmethod
    def get_completion_message_for_questions(total_answered: int, total_questions: int) -> str:
        """Get completion message after answering technical questions"""
        if total_answered == total_questions:
            return f"""🎉 **Excellent work!** 

You've successfully answered all {total_questions} technical questions. Your responses demonstrate good knowledge of your technical stack and show how you approach problems.

**What's Next:**
✅ Your technical assessment is complete
✅ All responses have been recorded
✅ Our team will review your answers along with your profile
✅ You'll hear from us within 48-72 hours if there's a good match

Thank you for taking the time to complete this comprehensive screening! 🌟"""
        else:
            return f"""**Progress Update:** {total_answered}/{total_questions} questions completed.

Ready for the next question? 🚀"""

    @staticmethod
    def get_question_validation_prompt() -> str:
        """Get prompt for validating question responses"""
        return """Please evaluate the candidate's response for:
1. Technical accuracy
2. Depth of understanding  
3. Practical experience
4. Communication clarity

Provide brief feedback on their answer quality."""

    @staticmethod
    def get_adaptive_question_prompt(previous_answers: List[str], remaining_tech: List[str]) -> str:
        """Generate adaptive question based on previous answers"""
        return f"""Based on the candidate's previous responses, generate a follow-up question that:
1. Builds on their demonstrated knowledge level
2. Explores technologies they haven't discussed yet: {', '.join(remaining_tech)}
3. Matches the complexity they've shown in previous answers
4. Provides insight into their practical experience

Previous answer quality indicates their knowledge level - adjust accordingly."""

    @staticmethod
    def format_question_summary(questions: List[Dict[str, Any]], responses: List[str]) -> str:
        """Format summary of questions and responses"""
        summary_parts = []

        for i, (question, response) in enumerate(zip(questions, responses), 1):
            category = question.get("category", "General").title()
            summary_parts.append(f"""**Q{i} ({category}):** {question['question']}
**Response:** {response[:200]}{'...' if len(response) > 200 else ''}
""")

        return "\n".join(summary_parts)

class QuestionFallbacks:
    """Fallback questions when tech stack is unclear"""

    GENERAL_TECH_QUESTIONS = [
        {
            "question": "What programming language are you most comfortable with and why?",
            "category": "general",
            "difficulty": "junior",
            "expected_topics": ["programming languages", "preferences", "experience"]
        },
        {
            "question": "Describe a challenging technical problem you've solved recently. What was your approach?",
            "category": "problem-solving",
            "difficulty": "mid",
            "expected_topics": ["problem-solving", "debugging", "methodology"]
        },
        {
            "question": "How do you approach learning new technologies or frameworks?",
            "category": "learning",
            "difficulty": "junior",
            "expected_topics": ["learning", "adaptation", "growth mindset"]
        },
        {
            "question": "What development tools and environments do you use in your daily work?",
            "category": "tools",
            "difficulty": "junior",
            "expected_topics": ["development tools", "workflow", "productivity"]
        },
        {
            "question": "How do you ensure the quality and reliability of your code?",
            "category": "quality",
            "difficulty": "mid",
            "expected_topics": ["testing", "code review", "best practices"]
        }
    ]

    @staticmethod
    def get_fallback_questions(experience_years: int) -> List[Dict[str, Any]]:
        """Get fallback questions based on experience level"""
        all_questions = QuestionFallbacks.GENERAL_TECH_QUESTIONS.copy()

        # Filter by experience level
        if experience_years <= 2:
            return [q for q in all_questions if q["difficulty"] in ["junior"]]
        elif experience_years <= 5:
            return [q for q in all_questions if q["difficulty"] in ["junior", "mid"]]
        else:
            return all_questions  # All questions for senior level
