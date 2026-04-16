# CursosDev Telegram Alert Bot

![Python](https://img.shields.io/badge/python-3.11-blue)
![License](https://img.shields.io/badge/license-MIT-green)

A GitHub Actions bot that automatically monitors CursosDev for new Udemy coupon courses and sends real-time notifications to Telegram.

It filters courses based on custom keywords such as kubernetes, k8s, python, devops, and ensures users are notified only when new relevant courses appear.

Repository:
https://github.com/sassenagh/telegram-bot

---

# Architecture

The system runs entirely on GitHub Actions with no server required.

It scrapes CursosDev periodically, filters results, compares them with previously seen courses, and sends alerts via Telegram.

```
     CursosDev Website
             │
             ▼
   GitHub Actions Scheduler
             │
             ▼
      Python Scraper Bot
             │
     ┌──────────────┐
     │ seen_courses │
     │   (state)    │
     └──────────────┘
             │
             ▼
      Telegram Bot API
```

---

# Features

- Automatic scraping of new Udemy coupon courses from CursosDev
- Keyword-based filtering
- Instant Telegram notifications
- Deduplication system to avoid repeated alerts
- Fully serverless (runs on GitHub Actions)
- Secrets-based configuration (no sensitive data exposed)
- Scheduled execution every 15 minutes
- Lightweight state persistence using repository file tracking

---

# Tech Stack

## Backend

- Python 3.11
- Requests
- BeautifulSoup4

## Infrastructure

- GitHub Actions (CI/CD scheduler)
- Telegram Bot API

---

# Project Structure

```
telegram-bot
│
├── script.py             # Main scraping + notification logic
├── seen_courses.json     # Stores previously sent courses
├── requirements.txt      # Dependencies
└── README.md
```

---

# How It Works

1. GitHub Actions triggers the workflow every 15 minutes
2. Python script downloads the CursosDev homepage
3. Extracts all course cards and links
4. Filters results using configured keywords
5. Compares against previously seen courses
6. Sends new matches to Telegram
7. Updates repository state (seen_courses.json)

---

# Configuration

All sensitive values are stored using GitHub Secrets.

## Required secrets:

- TELEGRAM_TOKEN → Telegram bot token
- CHAT_ID → Your Telegram chat ID
- KEYWORDS → Comma-separated list of keywords

Example:
kubernetes,k8s,python,devops

---

# Running Locally

Clone the repository:

```bash
git clone https://github.com/sassenagh/telegram-bot.git
cd telegram-bot
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run manually:

```bash
python script.py
GitHub Actions Workflow
```

The bot runs automatically using GitHub Actions...

---

# License

MIT License