import requests
from bs4 import BeautifulSoup
import os
import json
import subprocess

URL = "https://www.cursosdev.com/"
SEEN_FILE = "seen_courses.json"

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

KEYWORDS = os.getenv("KEYWORDS", "")
KEYWORDS = [k.strip().lower() for k in KEYWORDS.split(",") if k]


def load_seen():
    if os.path.exists(SEEN_FILE):
        with open(SEEN_FILE, "r") as f:
            return set(json.load(f))
    return set()


def save_seen(seen):
    with open(SEEN_FILE, "w") as f:
        json.dump(list(seen), f)


def get_courses():
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, "html.parser")

    courses = []

    for a in soup.find_all("a", href=True):
        link = a["href"]

        if "/coupons-udemy/" not in link:
            continue

        h2 = a.find("h2")
        if not h2:
            continue

        title = h2.text.strip()

        courses.append((title, link))

    return courses


def filter_courses(courses):
    filtered = []

    for title, link in courses:
        title_lower = title.lower()

        if any(keyword in title_lower for keyword in KEYWORDS):
            filtered.append((title, link))

    return filtered


def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

    data = {
        "chat_id": CHAT_ID,
        "text": message
    }

    requests.post(url, data=data)


def commit_and_push():
    subprocess.run(["git", "config", "user.name", "github-actions"])
    subprocess.run(["git", "config", "user.email", "actions@github.com"])

    subprocess.run(["git", "add", SEEN_FILE])
    subprocess.run(["git", "commit", "-m", "update seen courses"], check=False)
    subprocess.run(["git", "push"])


def main():
    seen = load_seen()

    courses = get_courses()
    filtered = filter_courses(courses)

    new_courses = []

    for title, link in filtered:
        if link not in seen:
            new_courses.append((title, link))
            seen.add(link)

    # TEST_MODE = os.getenv("TEST_MODE") == "true"

    # if TEST_MODE:
    #     send_telegram("✅ Test desde GitHub Actions")
    #     return
    
    for title, link in new_courses:
        message = f"🔥 Nuevo curso:\n{title}\n{link}"
        send_telegram(message)

    if new_courses:
        save_seen(seen)
        commit_and_push()


if __name__ == "__main__":
    main()