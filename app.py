import streamlit as st
import time

from src.config import (
    APP_TITLE,
    APP_SUBTITLE,
    APP_VERSION,
    RESPONSE_MODES,
    QUICK_QUESTIONS,
    DISCLAIMER_TEXT,
    get_gemini_api_key
)
from src.prompts import TEST_QUESTIONS
from src.chatbot import AcademicChatbot

# Page configuration
st.set_page_config(
    page_title="IU SOIT AI Chatbot | Indira University Pune",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS matching the Selection Poster Laptop Interface Mockup
CUSTOM_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .main .block-container {
        padding-top: 1.2rem;
        padding-bottom: 2rem;
        max-width: 1100px;
    }

    /* Header Banner */
    .header-banner {
        background: linear-gradient(135deg, #0d233a 0%, #1e3c72 50%, #2a5298 100%);
        color: white;
        padding: 1.6rem 2rem;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        margin-bottom: 1.2rem;
    }

    .header-banner h1 {
        margin: 0;
        font-size: 2.1rem;
        font-weight: 700;
        letter-spacing: -0.5px;
        color: #ffffff;
    }

    .header-banner p {
        margin: 0.4rem 0 0 0;
        font-size: 1.05rem;
        opacity: 0.9;
    }

    /* Status Badges */
    .status-badge-ok {
        display: inline-block;
        background-color: #198754;
        color: #ffffff;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.82rem;
        font-weight: 600;
        margin-top: 0.5rem;
    }

    .status-badge-err {
        display: inline-block;
        background-color: #dc3545;
        color: #ffffff;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.82rem;
        font-weight: 600;
        margin-top: 0.5rem;
    }

    /* Disclaimer Box */
    .disclaimer-box {
        background-color: #fff8e6;
        border-left: 4px solid #ffc107;
        color: #664d03;
        padding: 0.75rem 1rem;
        border-radius: 6px;
        font-size: 0.88rem;
        margin-bottom: 1.2rem;
    }

    /* Action Chip Buttons */
    .stButton button {
        border-radius: 8px;
        border: 1px solid #ced4da;
        transition: all 0.2s ease-in-out;
    }

    .stButton button:hover {
        border-color: #1e3c72;
        color: #1e3c72;
        background-color: #f0f4f9;
    }
</style>
"""

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


def init_session_state():
    """Initialize session state variables."""
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": (
                    "👋 **Welcome to Indira University SOIT AI Chatbot!**\n\n"
                    "I am your official assistant for the **School of Information Technology (SOIT), Pune**.\n\n"
                    "How can I help you today? You can ask me about:\n"
                    "- 📝 **Exam Guidelines & Hall Tickets**\n"
                    "- 📊 **Attendance Policy (75% Rule)**\n"
                    "- 📅 **Timetable & Class Schedules**\n"
                    "- 🏫 **SOIT Courses & Syllabus**\n"
                    "- 📚 **Library Timings & Borrowing**\n"
                    "- 📞 **Placement Cell & HOD Contact Info**"
                )
            }
        ]
    if "pending_prompt" not in st.session_state:
        st.session_state.pending_prompt = None


def render_header(api_configured: bool):
    """Render top header banner matching poster theme."""
    status_html = (
        '<span class="status-badge-ok">🟢 Connected to Gemini AI (SOIT Pune)</span>'
        if api_configured
        else '<span class="status-badge-err">🔴 API Key Missing</span>'
    )
    
    st.markdown(
        f"""
        <div class="header-banner">
            <h1>{APP_TITLE}</h1>
            <p>{APP_SUBTITLE}</p>
            <div>{status_html}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def render_sidebar() -> str:
    """Render sidebar navigation matching poster laptop mockup."""
    st.sidebar.markdown("### 🏛️ SOIT Navigation")
    
    # Quick Navigation Prompts matching Poster Mockup (Dashboard, Academics, Exams, etc.)
    nav_options = {
        "📊 Dashboard": "Overview of Indira University SOIT Pune campus facilities and helpdesk",
        "📝 Exams Guidelines": "What are the exam guidelines at Indira University SOIT Pune?",
        "📅 Timetable & Schedule": "What is the daily class schedule and timetable at SOIT?",
        "📊 Attendance (75% Rule)": "What is the attendance policy (75% rule) at SOIT?",
        "🏫 SOIT Courses & Syllabus": "What courses/programs are offered by SOIT Pune?",
        "📚 Library Rules": "What are the library timings and borrowing rules?",
        "📑 Assignments": "How are assignment submissions and late penalties handled?",
        "🎉 School Events": "What technical events and hackathons are organized by SOIT Pune?",
        "📞 Contact Support": "How can I contact the SOIT student helpdesk and HOD office?"
    }

    st.sidebar.caption("Category Quick Links:")
    for nav_title, nav_prompt in nav_options.items():
        if st.sidebar.button(nav_title, use_container_width=True):
            st.session_state.pending_prompt = nav_prompt
            st.rerun()

    st.sidebar.markdown("---")

    # 1. Response Mode Selection
    st.sidebar.subheader("🎯 Response Mode")
    selected_mode = st.sidebar.radio(
        "Explanation style:",
        options=list(RESPONSE_MODES.keys()),
        index=0
    )
    st.sidebar.caption(f"ℹ️ *{RESPONSE_MODES[selected_mode]}*")

    st.sidebar.markdown("---")

    # 2. 15 Benchmark Evaluation Suite
    with st.sidebar.expander("🧪 15 Selection Evaluation Questions", expanded=False):
        st.caption("Benchmark question set for evaluation:")
        selected_test = st.selectbox(
            "Evaluation Questions:",
            options=["-- Select a Question --"] + TEST_QUESTIONS,
            index=0
        )
        if selected_test != "-- Select a Question --":
            clean_q = selected_test.split(". ", 1)[-1]
            if st.button("🚀 Ask Evaluation Question", use_container_width=True):
                st.session_state.pending_prompt = clean_q
                st.rerun()

    st.sidebar.markdown("---")

    # 3. Clear Conversation Button
    if st.sidebar.button("🗑️ Clear Conversation", use_container_width=True, type="secondary"):
        st.session_state.messages = []
        st.session_state.pending_prompt = None
        st.toast("Conversation reset!", icon="🧹")
        st.rerun()

    st.sidebar.caption(f"SOIT Student AI Platform v{APP_VERSION}")
    return selected_mode


def render_quick_chips():
    """Render horizontal action chip buttons above chat input (matching poster mockup)."""
    st.write("**Quick Actions:**")
    col1, col2, col3, col4, col5, col6 = st.columns(6)

    chips = [
        (col1, "📅 Timetable", "What is the daily class schedule and timetable at SOIT?"),
        (col2, "📜 Syllabus", "What courses and syllabus options are offered by SOIT Pune?"),
        (col3, "📝 Exam Rules", "What are the exam guidelines at Indira University SOIT Pune?"),
        (col4, "📊 Attendance", "What is the attendance policy (75% rule) at SOIT?"),
        (col5, "🏫 SOIT Info", "Tell me about Indira University SOIT Pune campus and programs."),
        (col6, "📞 Contact", "How can I contact the SOIT student helpdesk and HOD office?")
    ]

    for col, label, prompt in chips:
        if col.button(label, use_container_width=True):
            st.session_state.pending_prompt = prompt
            st.rerun()


def main():
    init_session_state()

    # Initialize Chatbot Engine
    chatbot = AcademicChatbot()
    api_configured = chatbot.is_configured()

    # Render Header Banner & Sidebar
    render_header(api_configured)
    selected_mode = render_sidebar()

    # Disclaimer Box
    st.markdown(f'<div class="disclaimer-box">{DISCLAIMER_TEXT}</div>', unsafe_allow_html=True)

    # Missing API Key Warning if applicable
    if not api_configured:
        st.error(
            "🔑 **GEMINI_API_KEY is missing!**\n\n"
            "Add your key to the `.env` file in the project root:\n"
            "```bash\nGEMINI_API_KEY=your_actual_gemini_api_key\n```"
        )

    # Display Chat History
    for message in st.session_state.messages:
        avatar = "🎓" if message["role"] == "assistant" else "👤"
        with st.chat_message(message["role"], avatar=avatar):
            st.markdown(message["content"])

    # Render Quick Chips (Poster Mockup Style)
    render_quick_chips()

    # Handle Input Processing
    prompt_to_process = None

    if st.session_state.pending_prompt:
        prompt_to_process = st.session_state.pending_prompt
        st.session_state.pending_prompt = None

    chat_input_val = st.chat_input("Type your university question here (e.g., What are the exam guidelines?)...")
    if chat_input_val:
        prompt_to_process = chat_input_val

    if prompt_to_process:
        clean_prompt = prompt_to_process.strip()
        if not clean_prompt:
            st.warning("Please enter a valid question.")
            return

        # Add user message
        st.session_state.messages.append({"role": "user", "content": clean_prompt})
        with st.chat_message("user", avatar="👤"):
            st.markdown(clean_prompt)

        # Generate Assistant Response
        with st.chat_message("assistant", avatar="🎓"):
            with st.spinner(f"Fetching SOIT Pune AI Response ({selected_mode} Mode)..."):
                response_text, error_msg = chatbot.generate_response(
                    history=st.session_state.messages[:-1],
                    user_query=clean_prompt,
                    response_mode=selected_mode
                )

                if error_msg:
                    st.error(error_msg)
                elif response_text:
                    st.markdown(response_text)
                    st.session_state.messages.append({"role": "assistant", "content": response_text})


if __name__ == "__main__":
    main()
