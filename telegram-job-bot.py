import requests
import time
import os

BOT_TOKEN = os.getenv("BOT_TOKEN", "")
CHAT_ID = os.getenv("CHAT_ID", "5049534508")

KEYWORDS = ["python intern", "ai intern", "data science", "automation", "remote intern"]

SAMPLE_JOBS = [
    {"title": "Python Developer Intern", "company": "TechCorp", "location": "Remote", "link": "https://internshala.com/internship/python-developer"},
    {"title": "AI/ML Intern", "company": "DataMinds", "location": "Remote", "link": "https://internshala.com/internship/ai-ml"},
    {"title": "Automation Engineer Intern", "company": "AutoTech", "location": "Remote", "link": "https://internshala.com/internship/automation"},
    {"title": "Data Science Intern", "company": "AnalyticsPro", "location": "Remote", "link": "https://internshala.com/internship/data-science"},
    {"title": "Software Development Intern", "company": "WebWorks", "location": "Remote", "link": "https://internshala.com/internship/software-development"},
]

seen_jobs = set()

def send_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, json={
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "Markdown"
    })

def get_updates(offset=None):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates"
    try:
        resp = requests.get(url, params={"timeout": 30, "offset": offset})
        return resp.json().get("result", [])
    except:
        return []

def check_new_jobs():
    new_jobs = []
    for job in SAMPLE_JOBS:
        title_lower = job["title"].lower()
        if any(kw in title_lower for kw in KEYWORDS):
            if job["title"] not in seen_jobs:
                new_jobs.append(job)
                seen_jobs.add(job["title"])
    return new_jobs

send_message(
    "🚀 *Job Alert Bot Started!*\n\n"
    f"🔍 Watching for: {', '.join(KEYWORDS)}\n"
    "📬 I'll notify you when new jobs appear.\n\n"
    "Commands:\n"
    "/jobs — Show recent jobs\n"
    "/check — Force check now"
)

last_update_id = 0

while True:
    updates = get_updates(offset=last_update_id + 1)
    for update in updates:
        last_update_id = update["update_id"]
        msg = update.get("message", {})
        text = msg.get("text", "")

        if text == "/jobs":
            for job in SAMPLE_JOBS:
                send_message(
                    f"💼 *{job['title']}*\n"
                    f"🏢 {job['company']}\n"
                    f"📍 {job['location']}\n"
                    f"🔗 {job['link']}"
                )
        elif text == "/check":
            send_message("🔍 Checking for new jobs...")

    new_jobs = check_new_jobs()
    for job in new_jobs:
        send_message(
            f"🆕 *New Job Found!*\n\n"
            f"💼 *{job['title']}*\n"
            f"🏢 {job['company']}\n"
            f"📍 {job['location']}\n"
            f"🔗 {job['link']}"
        )

    time.sleep(60)
