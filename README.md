# TalentScout Hiring Assistant 🤖

A sophisticated AI-powered hiring assistant built with Streamlit and OpenRouter that conducts initial candidate screenings for technology positions. This application combines modern LLM capabilities with a robust, modular architecture to provide an engaging and effective recruitment experience.

## 📋 Table of Contents
- [Features](#features)
- [Architecture](#architecture)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [Testing](#testing)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [License](#license)

## ✨ Features

### Core Functionality
- **🎯 Intelligent Conversation Flow**: State-machine based conversation management
- **📝 Comprehensive Data Collection**: Systematic gathering of candidate information
- **🔧 Dynamic Technical Questions**: AI-generated questions based on candidate's tech stack
- **✅ Input Validation**: Robust validation using Pydantic models
- **💾 Data Persistence**: Secure storage of candidate profiles and responses
- **📊 Analytics Dashboard**: Real-time insights and candidate statistics

### User Experience
- **🎨 Beautiful UI**: Custom-styled Streamlit interface with responsive design
- **💬 Real-time Chat**: Smooth conversational experience
- **📈 Progress Tracking**: Visual progress indicators
- **🔄 Session Management**: Automatic save/restore functionality
- **🚨 Error Handling**: Graceful error recovery and user guidance

### Technical Features
- **🧠 LLM Integration**: OpenRouter API with multiple model support
- **🏗️ Modular Architecture**: Clean separation of concerns
- **📝 Structured Logging**: Comprehensive logging with structlog
- **🧪 Test Coverage**: Extensive unit tests with pytest
- **🔒 Data Privacy**: Secure handling of sensitive information
- **⚡ Performance**: Optimized for speed and scalability

## 🏗️ Architecture

### Project Structure
```
talentscout_hiring_assistant/
│
├── app.py                         # 🔹 Main Streamlit application
├── config/
│   └── settings.py                # 🔹 Environment configuration
│
├── prompts/
│   ├── greeting_prompt.py         # Welcome and introduction prompts
│   ├── info_prompt.py             # Data collection prompts
│   ├── tech_question_prompt.py    # Technical question generation
│   └── fallback_prompt.py         # Error handling and fallbacks
│
├── services/
│   ├── llm_service.py             # 🔹 OpenRouter LLM integration
│   ├── conversation_service.py    # Dialogue management
│   └── storage_service.py         # 🔹 Data persistence
│
├── models/
│   ├── candidate.py               # 🔹 Pydantic data models
│   └── session_state.py           # Session management schemas
│
├── utils/
│   ├── logger.py                  # 🔹 Structured logging
│   ├── constants.py               # Application constants
│   └── helpers.py                 # Utility functions
│
├── data/
│   └── candidates.json            # Local candidate database
│
├── tests/
│   ├── test_models.py             # Model validation tests
│   ├── test_services.py           # Service integration tests
│   └── test_prompts.py            # Prompt generation tests
│
├── requirements.txt               # 🔧 Dependencies
├── .env                          # 🔐 Environment variables
└── README.md                     # 📘 Documentation
```

### Core Components

#### 1. Conversation Management
- **State Machine**: Finite state machine for conversation flow
- **Context Awareness**: Maintains conversation context and user data
- **Input Validation**: Real-time validation of user responses
- **Error Recovery**: Intelligent error handling and retry mechanisms

#### 2. LLM Integration
- **OpenRouter API**: Access to multiple LLM providers
- **Dynamic Prompting**: Context-aware prompt engineering
- **Response Processing**: Structured response parsing and validation
- **Fallback Systems**: Automatic failover to backup models

#### 3. Data Management
- **Pydantic Models**: Type-safe data validation and serialization
- **JSON Storage**: Local file-based candidate database
- **Session Persistence**: Automatic save/restore functionality
- **Export Capabilities**: CSV export for data analysis

## 🚀 Installation

### Prerequisites
- Python 3.9 
- OpenRouter API key ([Get one here](https://openrouter.ai))
- Git (for cloning the repository)

### Step-by-Step Setup

1. **Clone the Repository**
   ```bash
   git clone https://github.com/piyush230502/talentscout-hiring-assistant.git
   cd talentscout-hiring-assistant
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv venv

   # On Windows
   conda create -p chatbot python=3.9 -y

   # On macOS/Linux
   source venv/bin/activate
   conda activate chatbot
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Configuration**
   ```bash
   # Copy the environment template
   cp .env.example .env

   # Edit .env with your settings
   nano .env
   ```

5. **Initialize Data Directory**
   ```bash
   mkdir -p data
   mkdir -p assets
   ```

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the root directory:

```env
# OpenRouter API Configuration
OPENROUTER_API_KEY=your_openrouter_api_key_here
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1

# Application Configuration
APP_NAME=TalentScout Hiring Assistant
DEBUG=false
LOG_LEVEL=INFO

# Model Configuration
DEFAULT_MODEL=openai/gpt-4-turbo-preview
FALLBACK_MODEL=openai/gpt-3.5-turbo
MAX_TOKENS=1500
TEMPERATURE=0.7

# Session Configuration
SESSION_TIMEOUT=3600
MAX_CONVERSATION_LENGTH=50
```

### API Key Setup

1. **Get OpenRouter API Key**:
   - Visit [OpenRouter.ai](https://openrouter.ai)
   - Sign up for an account
   - Navigate to API keys section
   - Generate a new API key
   - Copy the key to your `.env` file

2. **Configure Model Access**:
   - Ensure your API key has access to required models
   - Set up billing if using paid models
   - Test connectivity with a simple request

## 🎯 Usage

### Running the Application

1. **Start the Application**
   ```bash
   streamlit run app.py
   ```

2. **Access the Interface**
   - Open your browser to `http://localhost:8501`
   - The application will start with a welcome message

### User Journey

1. **Welcome & Introduction**: Candidate is greeted and briefed about the process
2. **Information Collection**: 
   - Full name
   - Email address
   - Phone number
   - Years of experience
   - Technical skills and expertise
3. **Technical Assessment**: AI-generated questions based on their tech stack
4. **Completion**: Summary and next steps information

### Admin Features

Enable admin panel in the sidebar to access:
- **📊 Dashboard**: Candidate statistics and analytics
- **👥 Candidate Management**: View and manage candidate profiles
- **📥 Data Export**: Export candidate data to CSV
- **🛠️ System Management**: Database cleanup and maintenance

## 📚 API Documentation

### Core Services

#### LLMService
```python
from services.llm_service import llm_service

# Generate technical questions
questions = llm_service.generate_technical_questions(
    tech_stack="Python, React, PostgreSQL",
    experience_years=5,
    candidate_name="John Smith"
)

# Process conversation
response = llm_service.generate_conversation_response(
    user_input="I have 5 years of Python experience",
    conversation_history=conversation_history,
    context={"current_state": "collecting_experience"}
)
```

#### ConversationService
```python
from services.conversation_service import ConversationService

# Initialize conversation
service = ConversationService(session_id="unique-session-id")

# Process user input
response, context = service.process_user_input(
    user_input="My name is John Smith",
    conversation_history=[]
)
```

#### StorageService
```python
from services.storage_service import storage_service

# Save candidate data
success = storage_service.save_candidate_data(
    candidate_data=candidate_info,
    session_id="session-123"
)

# Retrieve candidate
candidate = storage_service.get_candidate_by_email("john@example.com")

# Get statistics
stats = storage_service.get_database_stats()
```

### Model Schemas

#### CandidateInfo
```python
from models.candidate import CandidateInfo

candidate = CandidateInfo(
    name="John Smith",
    email="john.smith@email.com",
    phone="555-123-4567",
    experience_years=5,
    tech_stack="Python, Django, React, PostgreSQL"
)
```

## 🧪 Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html

# Run specific test file
pytest tests/test_models.py

# Run with verbose output
pytest -v
```

### Test Categories

- **Model Tests**: Pydantic model validation and serialization
- **Service Tests**: Business logic and API integration
- **Prompt Tests**: Prompt generation and formatting
- **Integration Tests**: End-to-end workflow testing

### Writing Tests

```python
import pytest
from models.candidate import CandidateInfo

def test_candidate_validation():
    """Test candidate info validation"""
    candidate = CandidateInfo(
        name="Test User",
        email="test@example.com",
        phone="555-123-4567",
        experience_years=3,
        tech_stack="Python, React"
    )
    assert candidate.name == "Test User"
    assert candidate.experience_years == 3
```

## 🚀 Deployment

### Streamlit Cloud

1. **Push to GitHub**:
   ```bash
   git add .
   git commit -m "Initial deployment"
   git push origin main
   ```

2. **Deploy on Streamlit Cloud**:
   - Visit [share.streamlit.io](https://share.streamlit.io)
   - Connect your GitHub repository
   - Configure environment variables
   - Deploy the application

3. **Environment Setup**:
   - Add `OPENROUTER_API_KEY` in Streamlit secrets
   - Configure other environment variables
   - Test the deployed application

### Docker Deployment

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

```bash
# Build and run
docker build -t talentscout-assistant .
docker run -p 8501:8501 --env-file .env talentscout-assistant
```

### Railway Deployment

## Deployment 

To deploy it to Railway, we need to:
1. Create a Procfile: This file tells Railway how to start the application.
2. Create a runtime.txt: This file specifies the Python version to use
3. Update requirements.txt: We need to add gunicorn to run the app in a production environment.
4. Add a .railway directory with a railway.json file: This is the modern way to configure Railway deployments and will contain the start command and other settings

5.make a ".railway" directory by using command "mkdir .railway"

-- Now, you can deploy your application to Railway by following these steps:

1. Install the Railway CLI: If you haven't already, install the Railway command-line interface.
2. Login to Railway: railway login
3. Initialize your project: railway init
4. Deploy: railway up
5. Railway will automatically detect the configuration files I've created and deploy your application.

### Production Considerations

- **Security**: Use environment variables for sensitive data
- **Monitoring**: Implement application monitoring and alerting
- **Scaling**: Consider load balancing for high traffic
- **Backup**: Regular database backups and disaster recovery
- **Performance**: Monitor API usage and optimize accordingly

## 🔧 Customization

### Adding New Tech Stacks

Edit `utils/constants.py`:

```python
TECH_STACK_CATEGORIES = {
    "your_category": {
        "technologies": ["Technology1", "Technology2"],
        "sample_questions": [
            "Your custom question here",
            "Another question"
        ]
    }
}
```

### Custom Prompts

Create new prompt files in `prompts/` directory:

```python
class CustomPrompts:
    """Your custom prompt collection"""

    @staticmethod
    def get_custom_prompt(context: dict) -> str:
        return f"Custom prompt with {context}"
```

### Extending Models

Add new Pydantic models in `models/`:

```python
from pydantic import BaseModel

class CustomModel(BaseModel):
    """Your custom data model"""
    field1: str
    field2: int
```

## 🤝 Contributing

We welcome contributions! Please follow these guidelines:

### Development Setup

1. **Fork the Repository**
2. **Create Feature Branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make Changes** and add tests
4. **Run Tests**:
   ```bash
   pytest
   ```
5. **Submit Pull Request**

### Code Standards

- **PEP 8**: Follow Python style guidelines
- **Type Hints**: Use type hints for all functions
- **Documentation**: Add docstrings to all functions
- **Testing**: Maintain test coverage above 80%
- **Logging**: Use structured logging for debugging

### Pull Request Process

1. **Update Documentation**: Update README if needed
2. **Add Tests**: Ensure new features have tests
3. **Check CI**: Ensure all checks pass
4. **Review Process**: Address review feedback
5. **Merge**: Squash and merge when approved

## 📊 Monitoring and Analytics

### Key Metrics

- **Conversation Completion Rate**: Percentage of started conversations that reach completion
- **Average Session Duration**: Time spent in the screening process
- **Question Response Quality**: Analysis of technical question responses
- **Technology Trends**: Most common tech stacks among candidates
- **User Experience**: Error rates and retry attempts

### Performance Monitoring

```python
# Monitor API response times
response_time = time.time() - start_time
logger.info("API call completed", response_time=response_time)

# Track conversation states
logger.info("State transition", 
           from_state=previous_state, 
           to_state=current_state,
           session_id=session_id)
```

## 🔐 Security Considerations

### Data Protection
- **Encryption**: Sensitive data encrypted at rest
- **API Keys**: Stored securely in environment variables
- **Input Validation**: All user inputs validated and sanitized
- **Session Management**: Secure session handling with timeouts

### Privacy Compliance
- **Data Minimization**: Collect only necessary information
- **Retention Policy**: Automatic cleanup of old data
- **Access Control**: Role-based access to candidate data
- **Audit Logging**: Complete audit trail of data access

## 🆘 Troubleshooting

### Common Issues

#### API Key Issues
```bash
# Check API key configuration
python -c "from config.settings import settings; print(settings.validate_api_key())"
```

#### Database Issues
```bash
# Reset database
rm data/candidates.json
# Restart application
```

#### Module Import Issues
```bash
# Ensure PYTHONPATH is set
export PYTHONPATH=.
streamlit run app.py
```

### Debugging

Enable debug mode in `.env`:
```env
DEBUG=true
LOG_LEVEL=DEBUG
```

Check logs for detailed information:
```python
from utils.logger import logger
logger.debug("Debug message", context={"key": "value"})
```

## 📈 Roadmap

### Upcoming Features

- **🌐 Multi-language Support**: International candidate support
- **📞 Voice Integration**: Voice-based interviews
- **🤖 Advanced AI**: GPT-4 Vision for resume analysis
- **📊 Advanced Analytics**: ML-powered candidate insights
- **🔗 CRM Integration**: Connect with existing HR systems
- **📱 Mobile App**: Native mobile application

### Version History

- **v1.0.0**: Initial release with core functionality
- **v1.1.0**: Enhanced UI and error handling
- **v1.2.0**: Admin panel and analytics (Planned)
- **v2.0.0**: Voice integration and mobile support (Planned)

## 📞 Support

### Getting Help

- **📖 Documentation**: Check this README and inline documentation
- **🐛 Issues**: Report bugs on GitHub Issues
- **💬 Discussions**: Join GitHub Discussions for questions
- **📧 Email**: Contact support@talentscout.ai

### Community

- **🌟 Star the Repository**: Show your support
- **🍴 Fork and Contribute**: Help improve the project
- **📢 Share**: Tell others about TalentScout

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Built with ❤️ by the TalentScout Team**

*Empowering recruiters with AI-driven candidate screening*
