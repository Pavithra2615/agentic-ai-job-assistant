import json

def search_jobs(skill):
    with open("jobs.json", "r") as f:
        jobs = json.load(f)

    matched = []

    for job in jobs:
        if skill.lower() in [s.lower() for s in job["skills"]]:
            matched.append(job)

    return matched


if __name__ == "__main__":
    result = search_jobs("Python")
    print(result)
