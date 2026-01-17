import os
import streamlit as st
import json
from openai import OpenAI
from job_search import search_jobs
from PyPDF2 import PdfReader
from gmail_sender import send_email

# ---------- OpenAI ----------
client = OpenAI()

st.set_page_config(page_title="Agentic AI Job Assistant")
st.title("🤖 Agentic AI Job Assistant")
st.write("Upload resume, find jobs, apply, track status, and send real emails.")

# ---------- Session Memory ----------
if "resume_skills" not in st.session_state:
    st.session_state.resume_skills = ""
if "last_recommendation" not in st.session_state:
    st.session_state.last_recommendation = ""

# ---------- Resume Upload ----------
st.subheader("📄 Upload Resume (PDF)")
uploaded_file = st.file_uploader("Upload PDF Resume", type=["pdf"])

resume_text = ""
if uploaded_file:
    reader = PdfReader(uploaded_file)
    for page in reader.pages:
        resume_text += page.extract_text() or ""
    st.text_area("Resume Content", resume_text, height=200)

# ---------- Analyze Resume ----------
if uploaded_file and st.button("Analyze Resume"):
    prompt = f"Extract only the technical skills from this resume. Return as comma separated list.\n\n{resume_text}"
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    st.session_state.resume_skills = response.choices[0].message.content
    st.success("🧠 Extracted Skills")
    st.write(st.session_state.resume_skills)

# ---------- Manual Skills ----------
skills_input = st.text_input("Or enter skills manually", "Python, Machine Learning")
final_skills = st.session_state.resume_skills if st.session_state.resume_skills else skills_input
st.info(f"🤖 Agent using: {final_skills}")

# ---------- Find Best Job ----------
if st.button("🔍 Find Best Job"):
    with open("user_profile.json") as f:
        user = json.load(f)

    skill_list = [s.strip() for s in final_skills.split(",") if s.strip()]

    all_jobs = []
    for s in skill_list:
        all_jobs.extend(search_jobs(s))

    prompt = f"""
    You are an autonomous AI Job Agent.
    User Profile: {user}
    Skills: {skill_list}
    Jobs: {all_jobs}
    Pick the best job and explain why.
    """
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    st.session_state.last_recommendation = response.choices[0].message.content
    st.subheader("💡 AI Recommendation")
    st.write(st.session_state.last_recommendation)

# ---------- Apply ----------
if st.session_state.last_recommendation and st.button("📝 Apply"):
    with open("user_profile.json") as f:
        user = json.load(f)

    cover_prompt = f"""
    Write a professional cover letter for this user.
    User: {user}
    Job: {st.session_state.last_recommendation}
    """
    cover = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": cover_prompt}]
    ).choices[0].message.content

    # ---- Send real email using Gmail API ----
    hr_email = user["email"]   # send to yourself for testing
    subject = "Job Application - Machine Learning Intern"
    body = f"""
Dear Hiring Team,

Please find my application below:

{cover}

Regards,
{user['name']}
"""

    send_email(hr_email, subject, body)

    # ---- Save application ----
    with open("applications.json") as f:
        apps = json.load(f)

    apps.append({
        "job": st.session_state.last_recommendation,
        "cover_letter": cover,
        "status": "Applied"
    })

    with open("applications.json", "w") as f:
        json.dump(apps, f, indent=4)

    st.success("✅ Application sent via Gmail API!")
    st.subheader("📄 Cover Letter")
    st.write(cover)

# ---------- Application Tracker ----------
st.subheader("📂 Application Tracker")
with open("applications.json") as f:
    apps = json.load(f)

if not apps:
    st.write("No applications yet.")
else:
    for i, app in enumerate(apps):
        st.markdown(f"### 🏢 Application {i+1}")
        st.write("**Job:**", app["job"])
        st.write("**Status:**", app["status"])

        c1, c2, c3 = st.columns(3)
        if c1.button("📞 Interview", key=f"int{i}"):
            apps[i]["status"] = "Interview Scheduled"
        if c2.button("✅ Selected", key=f"sel{i}"):
            apps[i]["status"] = "Selected"
        if c3.button("❌ Rejected", key=f"rej{i}"):
            apps[i]["status"] = "Rejected"

    with open("applications.json", "w") as f:
        json.dump(apps, f, indent=4)

# ---------- Career Dashboard ----------
st.subheader("📊 Career Dashboard")
total = len(apps)
interviews = len([a for a in apps if a["status"] == "Interview Scheduled"])
selected = len([a for a in apps if a["status"] == "Selected"])
rejected = len([a for a in apps if a["status"] == "Rejected"])

st.write("Total Applications:", total)
st.write("Interviews:", interviews)
st.write("Selected:", selected)
st.write("Rejected:", rejected)
