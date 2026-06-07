import os
import json
from pathlib import Path

import requests

TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

SENT_FILE = "sent_alerts.json"

URL = "https://wahis.woah.org/api/v1/pi/event/filtered-list?language=en"

TARGET_COUNTRIES = {
    "Saudi Arabia",
    "Jordan",
    "Iraq",
    "Kuwait",
    "Qatar",
    "Bahrain",
    "United Arab Emirates",
    "Oman",
    "Yemen",
    "Sudan",
    "Ethiopia",
    "Somalia",
    "Djibouti",
    "Turkey",
    "India",
    "Pakistan",
    "Brazil"
}


def load_sent():
    if not Path(SENT_FILE).exists():
        return []

    with open(SENT_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_sent(data):
    with open(SENT_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


payload = {
    "animalTypes": [],
    "countries": [],
    "eventIds": [],
    "eventStartDate": None,
    "eventStatuses": [],
    "firstDiseases": [],
    "pageNumber": 0,
    "pageSize": 50,
    "reasons": [],
    "reportIds": [],
    "reportStatuses": [],
    "reportTypes": ["IN"],
    "secondDiseases": [],
    "sortColumn": "submissionDate",
    "sortOrder": "desc",
    "submissionDate": None,
    "typeStatuses": []
}

response = requests.post(URL, json=payload, timeout=30)
response.raise_for_status()

data = response.json()

sent_alerts = load_sent()

new_events = []

for item in data.get("list", []):

    if item.get("country") not in TARGET_COUNTRIES:
        continue

    report_id = item["reportId"]

    if report_id in sent_alerts:
        continue

    new_events.append(item)

if not new_events:
    print("لا توجد تنبيهات جديدة")
    raise SystemExit()

message = "🔴 إنذارات حيوانية جديدة\n\n"

for item in new_events[:10]:

    message += (
        f"الدولة: {item['country']}\n"
        f"المرض: {item['disease']}\n"
        f"رقم الحدث: {item['eventId']}\n"
        f"الحالة: {item['eventStatus']}\n"
        f"التاريخ: {item['submissionDate'][:10]}\n"
        f"المصدر: WOAH\n\n"
    )

telegram_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

r = requests.post(
    telegram_url,
    json={
        "chat_id": CHAT_ID,
        "text": message
    },
    timeout=30
)

print("Telegram:", r.status_code)

if r.status_code == 200:
    for item in new_events:
        sent_alerts.append(item["reportId"])

    save_sent(sent_alerts)

    print("تم حفظ التنبيهات المرسلة")
