"""
TalentScout Hiring Assistant - Main Streamlit Application
A comprehensive AI-powered hiring assistant for initial candidate screening.
"""
import streamlit as st
import time
from datetime import datetime
from typing import Dict, Any

# Configure page
st.set_page_config(
    page_title="TalentScout Hiring Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Import services and utilities
from config.settings import settings
from services.llm_service import llm_service
from services.conversation_service import ConversationService
from services.storage_service import storage_service
from utils.helpers import generate_session_id
from utils.logger import logger
from models.session_state import StreamlitSessionState
from prompts.greeting_prompt import GreetingPrompts

def initialize_session_state():
    """Initialize Streamlit session state"""
    if "session_id" not in st.session_state:
        st.session_state.session_id = generate_session_id()

    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "conversation_service" not in st.session_state:
        st.session_state.conversation_service = ConversationService(st.session_state.session_id)

    if "initialized" not in st.session_state:
        st.session_state.initialized = False

    if "user_data" not in st.session_state:
        st.session_state.user_data = {}

    if "interview_completed" not in st.session_state:
        st.session_state.interview_completed = False

def load_custom_css():
    """Load custom CSS for better styling"""
    st.markdown("""
    <style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
    }

    .chat-container {
        max-height: 600px;
        overflow-y: auto;
        padding: 1rem;
        border: 1px solid #ddd;
        border-radius: 10px;
        background-color: #f9f9f9;
    }

    .user-message {
        background-color: #e3f2fd;
        padding: 0.8rem;
        border-radius: 15px;
        margin: 0.5rem 0;
        margin-left: 2rem;
        border-left: 4px solid #2196f3;
    }

    .assistant-message {
        background-color: #f3e5f5;
        padding: 0.8rem;
        border-radius: 15px;
        margin: 0.5rem 0;
        margin-right: 2rem;
        border-left: 4px solid #9c27b0;
    }

    .progress-bar {
        background-color: #e0e0e0;
        border-radius: 10px;
        padding: 3px;
        margin: 1rem 0;
    }

    .progress-fill {
        background: linear-gradient(90deg, #4caf50 0%, #45a049 100%);
        height: 20px;
        border-radius: 8px;
        transition: width 0.3s ease;
    }

    .status-badge {
        display: inline-block;
        padding: 0.25rem 0.5rem;
        border-radius: 15px;
        font-size: 0.8rem;
        font-weight: bold;
    }

    .status-active {
        background-color: #4caf50;
        color: white;
    }

    .status-waiting {
        background-color: #ff9800;
        color: white;
    }

    .status-completed {
        background-color: #2196f3;
        color: white;
    }

    .sidebar-stats {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }

    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 0.5rem 0;
    }
    </style>
    """, unsafe_allow_html=True)

def render_header():
    """Render the main header"""
    st.markdown("""
    <div class="main-header">
        <h1>🤖 TalentScout Hiring Assistant</h1>
        <p>AI-Powered Initial Candidate Screening</p>
    </div>
    """, unsafe_allow_html=True)

def render_sidebar():
    """Render the sidebar with session info and controls"""
    with st.sidebar:
        st.header("📊 Session Info")

        # Session details
        st.markdown(f"""
        <div class="sidebar-stats">
            <strong>Session ID:</strong><br>
            <code>{st.session_state.session_id[:8]}...</code><br><br>
            <strong>Status:</strong><br>
            <span class="status-badge status-active">Active</span>
        </div>
        """, unsafe_allow_html=True)

        # Progress tracking
        if hasattr(st.session_state.conversation_service, 'context'):
            context = st.session_state.conversation_service.context
            collected_data = context.collected_data
            required_fields = ["name", "email", "phone", "experience_years", "tech_stack"]

            completed_fields = sum(1 for field in required_fields if collected_data.get(field))
            progress = (completed_fields / len(required_fields)) * 100

            st.subheader("📈 Progress")
            st.progress(progress / 100)
            st.write(f"**{completed_fields}/{len(required_fields)}** fields completed")

            # Show collected data
            if collected_data:
                st.subheader("✅ Collected Info")
                for field, value in collected_data.items():
                    if value and field != "technical_questions" and field != "responses":
                        if field == "experience_years":
                            st.write(f"**Experience:** {value} years")
                        elif field == "tech_stack":
                            st.write(f"**Tech Stack:** {value[:50]}...")
                        else:
                            st.write(f"**{field.title()}:** {value}")

        # API Status
        st.subheader("🔧 System Status")
        if llm_service.is_available():
            st.success("✅ LLM Service: Ready")
        else:
            st.error("❌ LLM Service: Not Available")
            st.info("Please configure your OpenRouter API key in the .env file")

        # Database stats
        try:
            stats = storage_service.get_database_stats()
            st.subheader("📋 Database Stats")
            st.metric("Total Candidates", stats.get("total_candidates", 0))
            st.metric("Completed Interviews", stats.get("completed_interviews", 0))

            if stats.get("top_technologies"):
                st.write("**Top Technologies:**")
                for tech, count in stats["top_technologies"][:5]:
                    st.write(f"• {tech}: {count}")
        except:
            st.write("Database stats unavailable")

        # Action buttons
        st.subheader("⚙️ Actions")

        if st.button("🔄 Reset Conversation"):
            st.session_state.messages.clear()
            st.session_state.conversation_service.reset_conversation()
            st.session_state.user_data.clear()
            st.session_state.interview_completed = False
            #st.experimental_rerun()
            st.rerun()

        if st.button("💾 Save Progress"):
            if st.session_state.user_data:
                success = storage_service.save_candidate_data(
                    st.session_state.user_data, 
                    st.session_state.session_id
                )
                if success:
                    st.success("Progress saved!")
                else:
                    st.error("Failed to save progress")

        # Debug info (only in debug mode)
        if settings.DEBUG:
            st.subheader("🐛 Debug Info")
            if hasattr(st.session_state.conversation_service, 'context'):
                context = st.session_state.conversation_service.context
                st.write(f"**State:** {context.current_state.value}")
                st.write(f"**Awaiting:** {context.awaiting_field}")
                st.write(f"**Retries:** {context.retry_count}")

def render_chat_interface():
    """Render the main chat interface"""
    st.subheader("💬 Chat Interface")

    # Initialize conversation if needed
    if not st.session_state.initialized:
        initial_message = st.session_state.conversation_service.get_initial_message()
        st.session_state.messages.append({
            "role": "assistant",
            "content": initial_message,
            "timestamp": datetime.now().isoformat()
        })
        st.session_state.initialized = True

    # Display chat messages
    chat_container = st.container()
    with chat_container:
        for message in st.session_state.messages:
            role = message["role"]
            content = message["content"]

            if role == "user":
                st.markdown(f"""
                <div class="user-message">
                    <strong>You:</strong><br>
                    {content}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="assistant-message">
                    <strong>TalentScout Assistant:</strong><br>
                    {content}
                </div>
                """, unsafe_allow_html=True)

    # Chat input
    if not st.session_state.interview_completed:
        user_input = st.chat_input("Type your response here...")

        if user_input:
            # Add user message
            st.session_state.messages.append({
                "role": "user",
                "content": user_input,
                "timestamp": datetime.now().isoformat()
            })

            # Process user input
            try:
                with st.spinner("Processing your response..."):
                    response, context = st.session_state.conversation_service.process_user_input(
                        user_input, 
                        st.session_state.messages
                    )

                # Add assistant response
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response,
                    "timestamp": datetime.now().isoformat()
                })

                # Update user data from context
                if context and context.get("collected_data"):
                    st.session_state.user_data.update(context["collected_data"])

                # Check if interview is completed
                if context and context.get("current_state") == "completed":
                    st.session_state.interview_completed = True

                    # Auto-save completed interview
                    if st.session_state.user_data:
                        storage_service.save_candidate_data(
                            st.session_state.user_data,
                            st.session_state.session_id
                        )

                #st.experimental_rerun()
                st.rerun()

            except Exception as e:
                st.error(f"Error processing your input: {str(e)}")
                logger.error("Error in chat interface", error=str(e))
    else:
        st.success("🎉 Interview completed! Thank you for your time.")
        st.info("Your responses have been recorded and will be reviewed by our team.")

def render_admin_panel():
    """Render admin panel for viewing candidates (optional)"""
    if st.sidebar.checkbox("👑 Admin Panel", value=False):
        st.header("👑 Admin Panel")

        tab1, tab2, tab3 = st.tabs(["📊 Overview", "👥 Candidates", "⚙️ Management"])

        with tab1:
            st.subheader("Database Overview")
            stats = storage_service.get_database_stats()

            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Candidates", stats.get("total_candidates", 0))
            with col2:
                st.metric("Completed Interviews", stats.get("completed_interviews", 0))
            with col3:
                st.metric("Average Completion", f"{stats.get('average_completion', 0)}%")
            with col4:
                exp_dist = stats.get("experience_distribution", {})
                total_exp = sum(exp_dist.values())
                st.metric("Total Profiles", total_exp)

            # Experience distribution chart
            if exp_dist:
                st.subheader("Experience Level Distribution")
                st.bar_chart(exp_dist)

            # Top technologies
            if stats.get("top_technologies"):
                st.subheader("Top Technologies")
                tech_data = dict(stats["top_technologies"][:10])
                st.bar_chart(tech_data)

        with tab2:
            st.subheader("Recent Candidates")
            candidates = storage_service.get_all_candidates()

            if candidates:
                # Sort by interview date (most recent first)
                candidates.sort(key=lambda x: x.interview_date, reverse=True)

                for candidate in candidates[:10]:  # Show last 10
                    with st.expander(f"{candidate.candidate_info.name} - {candidate.candidate_info.email}"):
                        col1, col2 = st.columns(2)
                        with col1:
                            st.write(f"**Experience:** {candidate.candidate_info.experience_years} years")
                            st.write(f"**Phone:** {candidate.candidate_info.phone}")
                            st.write(f"**Interview Date:** {candidate.interview_date.strftime('%Y-%m-%d %H:%M')}")
                        with col2:
                            st.write(f"**Questions:** {candidate.technical_questions_count}")
                            st.write(f"**Responses:** {candidate.responses_count}")
                            st.write(f"**Completion:** {candidate.completion_percentage:.1f}%")

                        st.write(f"**Tech Stack:** {candidate.candidate_info.tech_stack}")
                        if candidate.notes:
                            st.write(f"**Notes:** {candidate.notes}")
            else:
                st.info("No candidates found in the database.")

        with tab3:
            st.subheader("Database Management")

            col1, col2 = st.columns(2)
            with col1:
                if st.button("📥 Export to CSV"):
                    csv_path = storage_service.export_candidates_csv()
                    if csv_path:
                        st.success(f"Exported to: {csv_path}")
                    else:
                        st.error("Export failed")

            with col2:
                if st.button("🗑️ Cleanup Old Sessions"):
                    cleaned = storage_service.cleanup_old_sessions(days_old=7)
                    st.success(f"Cleaned up {cleaned} old session files")

            if st.button("💾 Backup Database"):
                backup_path = storage_service.backup_database()
                if backup_path:
                    st.success(f"Backup created: {backup_path}")
                else:
                    st.error("Backup failed")

def check_api_configuration():
    """Check if API is properly configured"""
    if not settings.validate_api_key():
        st.error("⚠️ OpenRouter API key not configured!")
        st.info("""
        To use this application, you need to:
        1. Get an API key from OpenRouter.ai
        2. Add it to your .env file as OPENROUTER_API_KEY=your_key_here
        3. Restart the application
        """)
        st.stop()

def main():
    """Main application function"""
    # Load custom CSS
    load_custom_css()

    # Check API configuration
    check_api_configuration()

    # Initialize session state
    initialize_session_state()

    # Render header
    render_header()

    # Create layout
    col1, col2 = st.columns([3, 1])

    with col1:
        render_chat_interface()

    with col2:
        render_sidebar()

    # Admin panel (optional)
    render_admin_panel()

    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; font-size: 0.8rem;">
        TalentScout Hiring Assistant v1.0 | Built with ❤️ using Streamlit & OpenRouter
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
