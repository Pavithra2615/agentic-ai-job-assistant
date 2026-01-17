import os
from openai import OpenAI
import json
from job_search import search_jobs

# Create OpenAI client
client = OpenAI()

# Load Agent memory (user profile)
with open("user_profile.json") as f:
    user = json.load(f)

# Agent uses tool to search jobs
jobs = search_jobs("Python")

prompt = f"""
You are an AI Job Agent.

User Profile:
{user}

Available Jobs:
{jobs}

Choose the best job for this user.
Explain why.
"""

# Call GPT
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are an autonomous AI job assistant."},
        {"role": "user", "content": prompt}
    ]
)

print(response.choices[0].message.content)
