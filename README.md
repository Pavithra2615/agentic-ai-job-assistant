# 🤖 Agentic AI Job Assistant

An **Agentic AI system** that autonomously analyzes a user's resume, identifies skills, searches for suitable jobs, recommends the best match, applies for jobs via email, and tracks application status using memory and decision logic.

---

## 🚀 Project Overview

This project demonstrates **Agentic AI**, where an AI agent:
- Perceives user input (resume)
- Reasons using a Large Language Model (GPT)
- Plans decisions (best job selection)
- Acts (job recommendation, email application)
- Remembers past actions (application tracking)

Unlike a simple chatbot, this system performs **goal-oriented autonomous actions**.

---

## 🧠 Why This Is Agentic AI (Not Just ChatGPT)

| Feature | Present |
|------|------|
| Perception (Resume input) | ✅ |
| Reasoning (Skill extraction, job fit) | ✅ |
| Planning (Choosing best job) | ✅ |
| Action (Apply via email) | ✅ |
| Memory (Application tracker) | ✅ |

This makes the system **Agentic**, not just a prompt-based AI.

---

## 🏗️ System Architecture

1. **User Interface (Streamlit)**  
   - Resume upload  
   - Job recommendation display  
   - Application tracker dashboard  

2. **Perception Layer**  
   - Resume PDF parsed using PyPDF2  

3. **Reasoning Engine (GPT)**  
   - Skill extraction  
   - Job matching logic  
   - Cover letter generation  

4. **Tool Layer**  
   - Job search module  
   - Email automation module  

5. **Memory Layer**  
   - Stores applications and statuses in JSON  

---

## 🔄 Workflow

1. User uploads resume  
2. AI extracts skills  
3. Job search tool collects job options  
4. AI selects the best job  
5. AI generates cover letter  
6. Email is sent to recruiter  
7. Application status is tracked  

---

## 🛠️ Tech Stack

- Python
- Streamlit
- OpenAI GPT API
- PyPDF2
- Gmail SMTP
- JSON (memory storage)

---

## 📂 Project Structure

agentic-ai-job-assistant/
│
├── app.py # Streamlit UI & agent controller
├── agent_brain.py # Reasoning logic
├── job_search.py # Job search tool
├── gmail_sender.py # Email automation
├── applications.json # Memory (job status tracking)
├── README.md # Project documentation
└── .gitignore # Security exclusions

