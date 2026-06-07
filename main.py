import os
import requests

TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

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

events = []

for item in data.get("list", []):

    if item.get("country") not in TARGET_COUNTRIES:
        continue

    events.append(item)

if not events:
    print("No matching events found")
    raise SystemExit()

message = "🔴 إنذارات حيوانية جديدة\n\n"

for item in events[:10]:

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
print("Events sent:", len(events))
