# 🎓 Indira University SOIT AI Chatbot (Pune)

> Official Selection Task Demo Submission for the **IU Academic AI Bot Development Team**. Built for **Indira University - School of Information Technology (SOIT), Pune** using Python, Streamlit, and the official Google Gemini SDK (`google-genai`).

---

## 📌 Overview

This AI application is built specifically for the **Student Selection Task - School AI Platform Development Team**. It delivers an interactive, ChatGPT-like interface designed to answer basic and advanced **school/university-related questions** for Indira University SOIT Pune students, faculty, and visitors.

---

## ✨ Features (Matching Selection Poster Requirements)

- 💬 **Interactive Student AI Interface**: Modern Streamlit chat UI with user/assistant bubbles, loading indicators, and full conversational memory.
- 🏛️ **SOIT Domain Knowledge Base**: Grounded with official Indira University SOIT Pune details (Exam rules, 75% attendance criteria, courses, timetable, library timings, assignments, events, and contact support).
- 🏷️ **Poster Mockup Navigation & Quick Action Chips**:
  - `[ 📅 Timetable ]` `[ 📜 Syllabus ]` `[ 📝 Exam Rules ]` `[ 📊 Attendance ]` `[ 🏫 SOIT Info ]` `[ 📞 Contact ]`
- ⚙️ **4 Response Modes**: `Balanced`, `Simple Explanation`, `Exam-Oriented`, `Detailed`.
- 🧪 **Built-in 15 Evaluation Questions**: Test suite covering all major university administrative and academic query types.
- 🔑 **Secure Credentials**: Reads `GEMINI_API_KEY` safely from `.env` without exposing keys.
- 🧹 **One-Click Reset**: Clear conversation history anytime.

---

## 📐 Tech Stack & Architecture

```text
       ┌────────────────────────┐
       │      SOIT Student      │
       └───────────┬────────────┘
                   │  1. Ask University Question / Click Chip
                   ▼
       ┌────────────────────────┐
       │  Streamlit UI (app.py) │ (Sidebar Nav + Quick Action Chips)
       └───────────┬────────────┘
                   │  2. Inject SOIT Knowledge Context & History
                   ▼
       ┌────────────────────────┐
       │   Python Backend Engine│ (src/prompts.py & src/knowledge_base.py)
       └───────────┬────────────┘
                   │  3. Google Gemini API Call (gemini-3.6-flash)
                   ▼
       ┌────────────────────────┐
       │   Google Gemini API    │ (Official google-genai SDK)
       └───────────┬────────────┘
                   │  4. Grounded SOIT Answer & Guidelines
                   ▼
       ┌────────────────────────┐
       │  Streamlit Chat UI     │ (Rendered Markdown Response)
       └────────────────────────┘
```

---

## 🚀 How to Run

```powershell
cd C:\Users\Om\.gemini\antigravity\scratch\iu-academic-ai-assistant
.\.venv\Scripts\python.exe -m streamlit run app.py
```

Or activate the virtual environment:
```powershell
.\.venv\Scripts\Activate.ps1
python -m streamlit run app.py
```

---

## 🧪 15 Benchmark Evaluation Questions (SOIT Pune)

1. What are the exam guidelines at Indira University SOIT Pune?
2. What is the attendance policy (75% rule) at SOIT?
3. What courses/programs are offered by SOIT Pune?
4. How can I download my exam hall ticket?
5. What are the library timings and borrowing rules?
6. How are assignment submissions and late penalties handled?
7. Who do I contact for placement and internship support at SOIT Pune?
8. What is the policy for re-evaluation of exam papers?
9. What technical events and hackathons are organized by SOIT Pune?
10. What is the daily class schedule and timetable at SOIT?
11. What are the rules for computer labs at SOIT?
12. How do I apply for medical leave for attendance exemption?
13. Where is the SOIT HOD office and Exam section located?
14. What postgraduate (PG) programs are available at SOIT Pune?
15. How can I contact the SOIT student helpdesk and campus office?
