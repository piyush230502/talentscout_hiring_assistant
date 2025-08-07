"""
Constants used throughout the TalentScout application
"""
from enum import Enum
from typing import Dict, List

class ConversationState(Enum):
    """States for the conversation flow"""
    GREETING = "greeting"
    COLLECTING_NAME = "collecting_name"
    COLLECTING_EMAIL = "collecting_email"
    COLLECTING_PHONE = "collecting_phone"
    COLLECTING_EXPERIENCE = "collecting_experience"
    COLLECTING_TECH_STACK = "collecting_tech_stack"
    GENERATING_QUESTIONS = "generating_questions"
    AWAITING_TECH_ANSWERS = "awaiting_tech_answers"
    COMPLETED = "completed"
    ERROR = "error"

class UserRole(Enum):
    """User roles in the conversation"""
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"

# Tech stack categories and related questions
TECH_STACK_CATEGORIES = {
    "frontend": {
        "technologies": ["React", "Vue.js", "Angular", "JavaScript", "TypeScript", "HTML", "CSS", "Sass", "Bootstrap", "Tailwind CSS"],
        "sample_questions": [
            "What is the difference between React hooks and class components?",
            "How do you handle state management in a large React application?",
            "Explain the Virtual DOM and its benefits",
            "What are TypeScript generics and when would you use them?",
            "How do you optimize CSS for better performance?"
        ]
    },
    "backend": {
        "technologies": ["Python", "Java", "Node.js", "C#", "Ruby", "Go", "PHP", "Scala", "Kotlin"],
        "sample_questions": [
            "Explain the difference between SQL and NoSQL databases",
            "How do you handle authentication and authorization in web applications?",
            "What are design patterns and can you explain a few commonly used ones?",
            "How do you optimize database queries for better performance?",
            "Explain microservices architecture and its advantages"
        ]
    },
    "database": {
        "technologies": ["MySQL", "PostgreSQL", "MongoDB", "Redis", "Elasticsearch", "SQLite", "Oracle", "SQL Server"],
        "sample_questions": [
            "What is database normalization and why is it important?",
            "Explain ACID properties in databases",
            "How do you handle database migrations in production?",
            "What are indexes and how do they improve query performance?",
            "Explain the CAP theorem in distributed databases"
        ]
    },
    "cloud": {
        "technologies": ["AWS", "Azure", "Google Cloud", "Docker", "Kubernetes", "Terraform", "Jenkins"],
        "sample_questions": [
            "What are the benefits of containerization?",
            "How do you implement CI/CD pipelines?",
            "Explain Infrastructure as Code and its advantages",
            "What are the key considerations for cloud security?",
            "How do you monitor and log applications in the cloud?"
        ]
    },
    "mobile": {
        "technologies": ["React Native", "Flutter", "iOS", "Android", "Swift", "Kotlin", "Xamarin"],
        "sample_questions": [
            "What are the differences between native and cross-platform development?",
            "How do you handle app state management?",
            "Explain mobile app security best practices",
            "How do you optimize app performance for different devices?",
            "What are Progressive Web Apps and their advantages?"
        ]
    },
    "data": {
        "technologies": ["Python", "R", "SQL", "Pandas", "NumPy", "TensorFlow", "PyTorch", "Scikit-learn", "Spark"],
        "sample_questions": [
            "Explain the difference between supervised and unsupervised learning",
            "How do you handle missing data in a dataset?",
            "What is overfitting and how do you prevent it?",
            "Explain the bias-variance tradeoff",
            "How do you evaluate the performance of a machine learning model?"
        ]
    }
}

# Common interview questions by experience level
EXPERIENCE_LEVEL_QUESTIONS = {
    "junior": [
        "What motivated you to pursue a career in technology?",
        "How do you approach learning new technologies?",
        "Describe a challenging problem you solved recently",
        "What development tools do you use daily?",
        "How do you debug your code?"
    ],
    "mid": [
        "How do you ensure code quality in your projects?",
        "Describe your experience with version control systems",
        "How do you handle technical debt?",
        "What testing strategies do you employ?",
        "How do you stay updated with industry trends?"
    ],
    "senior": [
        "How do you mentor junior developers?",
        "Describe your approach to system design",
        "How do you handle technical decision-making?",
        "What strategies do you use for scaling applications?",
        "How do you contribute to technical architecture decisions?"
    ]
}

# Fallback responses
FALLBACK_RESPONSES = [
    "I'm sorry, I didn't quite understand that. Could you please rephrase your response?",
    "Let me clarify - could you provide more details about that?",
    "I want to make sure I capture your information correctly. Could you elaborate on that?",
    "That's interesting! Could you give me a bit more context?",
    "I'd like to understand better. Could you explain that in a different way?"
]

# Exit keywords
EXIT_KEYWORDS = ["quit", "exit", "bye", "goodbye", "stop", "end", "cancel", "terminate"]

# Field validation patterns
VALIDATION_PATTERNS = {
    "email": r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",
    "phone": r"^[\+]?[1-9][\d]{0,15}$",
    "name": r"^[a-zA-Z\s\-\.']{2,50}$"
}

# Response templates
RESPONSE_TEMPLATES = {
    "welcome": "Welcome to TalentScout! I'm your AI hiring assistant, and I'm here to help with your initial screening process.",
    "data_collection_complete": "Thank you for providing all the information! Now let me generate some technical questions based on your expertise.",
    "interview_complete": "Thank you for completing the screening! Your responses have been recorded and will be reviewed by our hiring team.",
    "error": "I apologize, but I encountered an error. Let me try to help you in a different way.",
    "timeout": "It seems like our conversation has been inactive for a while. Feel free to start a new session when you're ready!"
}

# Company information (customizable)
COMPANY_INFO = {
    "name": "TalentScout",
    "description": "A leading recruitment agency specializing in technology placements",
    "focus": "We help connect talented individuals with innovative companies",
    "process": "Our screening process is designed to understand your skills and match you with the right opportunities"
}
