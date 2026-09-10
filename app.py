import streamlit as st
import os
import logging
from typing import List, Dict, Tuple, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("IUSOITBot")

# Import Google GenAI SDK
try:
    from google import genai
    from google.genai import types
    from google.genai.errors import APIError
    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False

# ===================================================================
# APP CONFIGURATION & CONSTANTS
# ===================================================================
APP_TITLE = "🎓 Indira University SOIT AI Chatbot"
APP_SUBTITLE = "School of Information Technology (SOIT), Pune — Official Student AI Platform"
APP_VERSION = "1.0.0"
DEFAULT_MODEL = "gemini-3.6-flash"
FALLBACK_MODELS = ["gemini-2.5-flash"]

RESPONSE_MODES = {
    "Balanced": "Clear, direct university explanation with key guidelines.",
    "Simple Explanation": "Beginner-friendly summary of school rules and academic procedures.",
    "Exam-Oriented": "Structured for exam preparation, exam rules, hall tickets, and syllabus.",
    "Detailed": "In-depth breakdown of university policies, course structures, and campus procedures."
}

DISCLAIMER_TEXT = (
    "⚠️ **Official Student AI Assistant**: Information is provided based on Indira University SOIT Pune guidelines. "
    "For official circulars, verify on the university portal (`portal.indira.edu`) or at the HOD Office."
)

# ===================================================================
# INDIRA UNIVERSITY SOIT PUNE KNOWLEDGE BASE
# ===================================================================
SOIT_KNOWLEDGE_BASE = """
===================================================================
INDIRA UNIVERSITY - SCHOOL OF INFORMATION TECHNOLOGY (SOIT), PUNE
OFFICIAL STUDENT KNOWLEDGE BASE & CAMPUS DIRECTORY
===================================================================

1. EXAM RULES & GUIDELINES:
- **Mandatory Identification**: Students must carry their valid Indira University Physical ID Card and Exam Hall Ticket to every examination.
- **Punctuality**: Students must arrive at the examination hall at least 15 minutes before the scheduled time. No entry is permitted 30 minutes after the exam starts.
- **Prohibited Items**: Smartwatches, mobile phones, programmable calculators, electronic devices, books, and loose sheets are strictly forbidden in the exam hall.
- **Attendance Eligibility**: Minimum 75% aggregate attendance is mandatory to be eligible to appear for Term-End Examinations.
- **Hall Ticket Download**: Hall tickets can be downloaded from the Indira University Student Portal (portal.indira.edu) 7 days prior to commencement.
- **Re-evaluation Policy**: Re-valuation or re-checking applications can be submitted online within 10 days of result publication.

2. ATTENDANCE POLICY:
- **Minimum Requirement**: 75% attendance is compulsory in each theory and practical subject.
- **Medical Leave**: Absence due to medical reasons requires a certified doctor's medical certificate submitted to the HOD Office within 3 working days of resuming classes.
- **Shortage Action**: Students with attendance between 60%-74% must submit extra assignments subject to Principal/HOD approval. Below 60% results in exam debarment.

3. ACADEMIC PROGRAMS & COURSES OFFERED AT SOIT PUNE:
- **Undergraduate (UG)**:
  - B.Tech in Computer Science & Engineering (CSE) - 4 Years
  - B.Tech in Information Technology (IT) - 4 Years
  - B.Sc. in Information Technology (B.Sc. IT) - 3 Years
  - B.Sc. in Cyber Security & Data Science - 3 Years
- **Postgraduate (PG)**:
  - Master of Computer Applications (MCA) - 2 Years
  - M.Sc. in Data Science & Artificial Intelligence - 2 Years
  - M.Sc. in Information Technology - 2 Years

4. TIMETABLE & CLASS SCHEDULE:
- **Class Hours**: Regular classes run Monday to Friday, 9:00 AM to 4:30 PM.
- **Lunch Break**: 12:30 PM to 1:15 PM daily.
- **Practicals / Labs**: Scheduled in 2-hour slots in SOIT Advanced Computing Labs.
- **Saturday Schedule**: Reserved for Industry Guest Lectures, Hackathons, Remedial Classes, and Student Club activities (9:00 AM to 1:00 PM).

5. LIBRARY & LEARNING RESOURCE CENTER:
- **Operating Hours**: Monday to Saturday, 8:00 AM to 8:00 PM (Extended till 10:00 PM during exam months).
- **Borrowing Limit**: UG students can borrow up to 3 books for 14 days; PG students up to 5 books.
- **Digital Library**: Access to IEEE Xplore, ACM Digital Library, SpringerLink, and NPTEL videos via campus Wi-Fi or student login.

6. ASSIGNMENTS & CONTINUOUS EVALUATION:
- **Internal Weightage**: Internal Continuous Assessment carries 40% weightage; Term-End Exam carries 60%.
- **Submission Mode**: Assignments must be submitted on the SOIT LMS Portal (lms.indira.edu) before 11:59 PM on the deadline date.
- **Late Penalty**: 10% mark deduction per day for late submissions up to 3 days; zero thereafter.

7. SCHOOL EVENTS & TECHNICAL CLUBS:
- **Technovision**: Annual SOIT National Level Technical Symposium & Hackathon held in February.
- **CodeBlitz**: Monthly intra-departmental competitive coding challenge.
- **Student Clubs**: SOIT Coding Club, AI & Robotics Society, Cyber Security Cell, WebDev Guild.

8. PLACEMENT CELL & CAREER SUPPORT:
- **SOIT Corporate Relations Cell**: Facilitates campus recruitments, internships, and industrial visits.
- **Top Recruiters**: TCS, Infosys, Wipro, Cognizant, Capgemini, Tech Mahindra, L&T Infotech, Quick Heal, Veritas Pune.
- **Placement Training**: Aptitude coaching, soft skills training, mock technical interviews, and resume building workshops conducted from 5th semester onwards.

9. CAMPUS ADDRESS & CONTACT SUPPORT:
- **Campus Address**: Indira University Pune, School of Information Technology (SOIT), Universe Campus, Tathawade, Pune - 411033, Maharashtra, India.
- **Student Helpdesk Email**: soit.support@indira.edu / helpdesk@indira.edu
- **Phone**: +91-020-66759400 / +91-020-66759500
- **HOD Office**: Room 204, 2nd Floor, SOIT Academic Block.
- **Exam Section**: Room 108, Ground Floor, Administrative Building.
"""

# System Instruction
SYSTEM_INSTRUCTION = f"""You are the official "Indira University SOIT AI Assistant" for the School of Information Technology (SOIT), Indira University, Pune.

Your primary role is to assist students, faculty, and visitors with accurate information regarding university procedures, school rules, academic guidelines, exam rules, timetables, course details, library rules, events, and campus facilities.

OFFICIAL INDIRA UNIVERSITY SOIT PUNE KNOWLEDGE BASE:
{SOIT_KNOWLEDGE_BASE}

CORE INSTRUCTIONS & OPERATIONAL RULES:
1. Answer all school and university-related questions accurately based on the provided SOIT Knowledge Base above.
2. For questions regarding Exam Guidelines, emphasize carrying the physical ID card, arriving on time, and the 75% attendance requirement.
3. For academic concept questions (e.g., Computer Science, Programming, Data Science, AI), answer clearly and helpfully with code examples and structured explanations.
4. If asked about specific administrative details NOT covered in the knowledge base (e.g., individual student marks, secret faculty phone numbers), state clearly:
   "I don't have access to private student records or unannounced circulars. Please check the official Indira University portal (portal.indira.edu) or contact the HOD Office at soit.support@indira.edu."
5. Maintain a professional, polite, and helpful tone representing Indira University SOIT Pune.
"""

MODE_DIRECTIVES = {
    "Balanced": "\nRESPONSE FORMAT DIRECTIVE (Balanced Mode):\nProvide a clear, well-structured response with key university guidelines, bullet points, and helpful next steps.\n",
    "Simple Explanation": "\nRESPONSE FORMAT DIRECTIVE (Simple Explanation Mode):\nSummarize the university rules or procedures in simple, easy-to-understand terms. Use clear bullet points and avoid unnecessary bureaucratic language.\n",
    "Exam-Oriented": "\nRESPONSE FORMAT DIRECTIVE (Exam-Oriented Mode):\nFormat your response specifically for exam preparation or exam conduct:\n- **Core Exam Rule / Concept**: Concise summary.\n- **Key Guidelines**: Mandatory requirements (ID Card, Hall Ticket, 75% attendance).\n- **Prohibited Items / Warnings**: What to avoid.\n- **Step-by-step Action**: How to proceed (e.g., download hall ticket, contact exam section).\n",
    "Detailed": "\nRESPONSE FORMAT DIRECTIVE (Detailed Mode):\nProvide an exhaustive breakdown including exact policies, contact emails, office locations, timings, course structures, and submission deadlines.\n"
}

TEST_QUESTIONS = [
    "1. What are the exam guidelines at Indira University SOIT Pune?",
    "2. What is the attendance policy (75% rule) at SOIT?",
    "3. What courses/programs are offered by SOIT Pune?",
    "4. How can I download my exam hall ticket?",
    "5. What are the library timings and borrowing rules?",
    "6. How are assignment submissions and late penalties handled?",
    "7. Who do I contact for placement and internship support at SOIT Pune?",
    "8. What is the policy for re-evaluation of exam papers?",
    "9. What technical events and hackathons are organized by SOIT Pune?",
    "10. What is the daily class schedule and timetable at SOIT?",
    "11. What are the rules for computer labs at SOIT?",
    "12. How do I apply for medical leave for attendance exemption?",
    "13. Where is the SOIT HOD office and Exam section located?",
    "14. What postgraduate (PG) programs are available at SOIT Pune?",
    "15. How can I contact the SOIT student helpdesk and campus office?"
]


def get_api_key() -> Optional[str]:
    """Retrieve GEMINI_API_KEY from Streamlit secrets or environment variables."""
    try:
        if "GEMINI_API_KEY" in st.secrets and st.secrets["GEMINI_API_KEY"]:
            return str(st.secrets["GEMINI_API_KEY"]).strip()
    except Exception:
        pass
    api_key = os.getenv("GEMINI_API_KEY")
    if api_key:
        return api_key.strip()
    return None


class AcademicChatbot:
    def __init__(self):
        self.api_key = get_api_key()
        self.client = None
        if GENAI_AVAILABLE and self.api_key:
            try:
                self.client = genai.Client(api_key=self.api_key)
            except Exception as e:
                logger.error(f"Failed to initialize Gemini Client: {e}")

    def is_configured(self) -> bool:
        return self.client is not None and bool(self.api_key)

    def generate_response(
        self,
        history: List[Dict[str, str]],
        user_query: str,
        response_mode: str = "Balanced"
    ) -> Tuple[Optional[str], Optional[str]]:
        if not user_query or not user_query.strip():
            return None, "Please enter a valid question."

        if not self.is_configured():
            return None, "🔑 **API Key Missing**: `GEMINI_API_KEY` is not configured in Streamlit Secrets."

        mode_directive = MODE_DIRECTIVES.get(response_mode, MODE_DIRECTIVES["Balanced"])
        full_system_instruction = f"{SYSTEM_INSTRUCTION}\n\n{mode_directive}"

        contents = []
        for msg in history:
            role = "user" if msg["role"] == "user" else "model"
            contents.append(types.Content(role=role, parts=[types.Part.from_text(text=msg["content"])]))
        contents.append(types.Content(role="user", parts=[types.Part.from_text(text=user_query)]))

        config = types.GenerateContentConfig(
            system_instruction=full_system_instruction,
            temperature=0.7,
            top_p=0.95,
        )

        models_to_try = [DEFAULT_MODEL] + FALLBACK_MODELS
        last_exception = None

        for model in models_to_try:
            try:
                logger.info(f"Generating response using model: {model}")
                response = self.client.models.generate_content(
                    model=model,
                    contents=contents,
                    config=config
                )
                if response and response.text:
                    return response.text, None
            except APIError as e:
                logger.warning(f"APIError with model {model}: {e}")
                last_exception = e
                continue
            except Exception as e:
                logger.error(f"Unexpected error with model {model}: {e}")
                last_exception = e
                break

        error_msg = str(last_exception) if last_exception else "Unknown error"
        if "API_KEY_INVALID" in error_msg or "invalid" in error_msg.lower() and "key" in error_msg.lower():
            return None, "❌ **Invalid API Key**: Your `GEMINI_API_KEY` appears invalid. Please check Streamlit Secrets."
        elif "RESOURCE_EXHAUSTED" in error_msg or "quota" in error_msg.lower():
            return None, "⚠️ **Rate Limit Exceeded**: Gemini API quota limit reached. Please wait a moment and try again."
        else:
            return None, f"⚠️ **Service Error**: Unable to connect to Gemini API. Details: {error_msg}"


# ===================================================================
# STREAMLIT UI LAYOUT
# ===================================================================
st.set_page_config(
    page_title="IU SOIT AI Chatbot | Indira University Pune",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

CUSTOM_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .main .block-container { padding-top: 1.2rem; padding-bottom: 2rem; max-width: 1100px; }
    .header-banner {
        background: linear-gradient(135deg, #0d233a 0%, #1e3c72 50%, #2a5298 100%);
        color: white; padding: 1.6rem 2rem; border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1); margin-bottom: 1.2rem;
    }
    .header-banner h1 { margin: 0; font-size: 2.1rem; font-weight: 700; color: #ffffff; }
    .header-banner p { margin: 0.4rem 0 0 0; font-size: 1.05rem; opacity: 0.9; }
    .status-badge-ok { display: inline-block; background-color: #198754; color: white; padding: 0.25rem 0.75rem; border-radius: 20px; font-size: 0.82rem; font-weight: 600; margin-top: 0.5rem; }
    .status-badge-err { display: inline-block; background-color: #dc3545; color: white; padding: 0.25rem 0.75rem; border-radius: 20px; font-size: 0.82rem; font-weight: 600; margin-top: 0.5rem; }
    .disclaimer-box { background-color: #fff8e6; border-left: 4px solid #ffc107; color: #664d03; padding: 0.75rem 1rem; border-radius: 6px; font-size: 0.88rem; margin-bottom: 1.2rem; }
    .stButton button { border-radius: 8px; border: 1px solid #ced4da; transition: all 0.2s ease-in-out; }
    .stButton button:hover { border-color: #1e3c72; color: #1e3c72; background-color: #f0f4f9; }
</style>
"""

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


def init_session_state():
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


def render_sidebar() -> str:
    st.sidebar.markdown("### 🏛️ SOIT Navigation")
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

    st.sidebar.subheader("🎯 Response Mode")
    selected_mode = st.sidebar.radio("Explanation style:", options=list(RESPONSE_MODES.keys()), index=0)
    st.sidebar.caption(f"ℹ️ *{RESPONSE_MODES[selected_mode]}*")

    st.sidebar.markdown("---")

    with st.sidebar.expander("🧪 15 Selection Evaluation Questions", expanded=False):
        selected_test = st.selectbox("Evaluation Questions:", options=["-- Select a Question --"] + TEST_QUESTIONS, index=0)
        if selected_test != "-- Select a Question --":
            clean_q = selected_test.split(". ", 1)[-1]
            if st.button("🚀 Ask Evaluation Question", use_container_width=True):
                st.session_state.pending_prompt = clean_q
                st.rerun()

    st.sidebar.markdown("---")

    if st.sidebar.button("🗑️ Clear Conversation", use_container_width=True, type="secondary"):
        st.session_state.messages = []
        st.session_state.pending_prompt = None
        st.toast("Conversation reset!", icon="🧹")
        st.rerun()

    st.sidebar.caption(f"SOIT Student AI Platform v{APP_VERSION}")
    return selected_mode


def main():
    init_session_state()
    chatbot = AcademicChatbot()
    api_configured = chatbot.is_configured()

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

    selected_mode = render_sidebar()
    st.markdown(f'<div class="disclaimer-box">{DISCLAIMER_TEXT}</div>', unsafe_allow_html=True)

    if not api_configured:
        st.error("🔑 **GEMINI_API_KEY is missing!** Please add `GEMINI_API_KEY = \"...\"` in Streamlit Cloud Secrets.")

    for message in st.session_state.messages:
        avatar = "🎓" if message["role"] == "assistant" else "👤"
        with st.chat_message(message["role"], avatar=avatar):
            st.markdown(message["content"])

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

        st.session_state.messages.append({"role": "user", "content": clean_prompt})
        with st.chat_message("user", avatar="👤"):
            st.markdown(clean_prompt)

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
