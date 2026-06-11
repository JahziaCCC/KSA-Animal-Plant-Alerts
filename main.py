import os
import json
from pathlib import Path

import requests

TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

SENT_FILE = "sent_alerts.json"

URL = "https://wahis.woah.org/api/v1/pi/event/filtered-list?language=en"

COUNTRIES_AR = {
    "Saudi Arabia": "السعودية",
    "Jordan": "الأردن",
    "Iraq": "العراق",
    "Kuwait": "الكويت",
    "Qatar": "قطر",
    "Bahrain": "البحرين",
    "United Arab Emirates": "الإمارات",
    "Oman": "عُمان",
    "Yemen": "اليمن",
    "Sudan": "السودان",
    "Ethiopia": "إثيوبيا",
    "Somalia": "الصومال",
    "Djibouti": "جيبوتي",
    "Turkey": "تركيا",
    "India": "الهند",
    "Pakistan": "باكستان",
    "Brazil": "البرازيل"
}

STATUS_AR = {
    "On-going": "نشط",
    "Resolved": "منتهي",
    "Stable": "مستقر",
    "Closed": "مغلق"
}

DISEASES_AR = {
    "High pathogenicity avian influenza viruses (Inf. with) (poultry)": "إنفلونزا الطيور عالية الضراوة",
    "Foot and mouth disease virus": "الحمى القلاعية",
    "Rabies virus (Inf. with)": "داء الكلب",
    "African swine fever virus (Inf. with)": "حمى الخنازير الإفريقية",
    "Newcastle disease virus (Inf. with)": "مرض النيوكاسل",
    "Lumpy skin disease virus (Inf. with)": "مرض الجلد العقدي",
    "Peste des petits ruminants virus (Inf. with)": "طاعون المجترات الصغيرة",
    "Rift Valley fever virus": "حمى الوادي المتصدع",
    "Bluetongue virus": "مرض اللسان الأزرق",
    "Camelpox virus": "جدري الإبل",
    "Sheep pox and goat pox virus": "جدري الأغنام والماعز",
    "Middle East respiratory syndrome coronavirus (MERS-CoV)": "متلازمة الشرق الأوسط التنفسية",
    "West Nile fever virus": "حمى غرب النيل"
}

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
    "reportTypes": ["IN", "FUR", "FR"],
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

    unique_id = f"{item['reportId']}_{item['reportType']}"

    if unique_id in sent_alerts:
        continue

    new_events.append(item)

if not new_events:
    print("لا توجد تنبيهات جديدة")
    raise SystemExit()

message = ""

for item in new_events[:10]:

    country = COUNTRIES_AR.get(
        item["country"],
        item["country"]
    )

    disease_raw = item["disease"].strip()

    disease = DISEASES_AR.get(
        disease_raw,
        disease_raw
    )

    status = STATUS_AR.get(
        item["eventStatus"],
        item["eventStatus"]
    )

    report_type = item.get("reportType", "")

    if report_type == "IN":
        icon = "🔴"
        title = "إنذار حيواني جديد"

    elif report_type == "FUR":
        icon = "🟠"
        title = "تحديث رسمي"

    elif report_type == "FR":
        icon = "🟢"
        title = "تقرير نهائي / احتواء"

    else:
        icon = "⚪"
        title = report_type

    message += (
        f"{icon} {title}\n\n"
        f"الدولة: {country}\n"
        f"المرض: {disease}\n"
        f"رقم الحدث: {item['eventId']}\n"
        f"الحالة: {status}\n"
        f"التاريخ: {item['submissionDate'][:10]}\n"
        f"المصدر: WOAH\n\n"
        f"━━━━━━━━━━━━━━\n\n"
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
        unique_id = f"{item['reportId']}_{item['reportType']}"
        sent_alerts.append(unique_id)

    save_sent(sent_alerts)

    print("تم حفظ التنبيهات المرسلة")
