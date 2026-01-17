import os
from openai import OpenAI
import json
from job_search import search_jobs

client = OpenAI()

with open("user_profile.json") as f:
    user = json.load(f)

skills = user["skills"]

def get_best_job(jobs):
    prompt = f"""
User Skills: {skills}
Jobs: {jobs}

From these jobs choose the best one.
If no job matches well, say: "NO MATCH"
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are an autonomous job matching AI."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content

# Agent loop
search_terms = ["Python", "Machine Learning", "AI", "Data Science"]

for term in search_terms:
    print(f"\n🔍 Searching for {term} jobs...")
    jobs = search_jobs(term)
    
    decision = get_best_job(jobs)
    print("🧠 AI Decision:", decision)

    if "NO MATCH" not in decision:
        print("\n✅ Suitable job found!")
        break
