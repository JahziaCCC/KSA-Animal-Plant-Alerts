import requests

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

def fetch_events():
    response = requests.get(URL, timeout=30)
    response.raise_for_status()

    data = response.json()

    events = []

    for item in data.get("list", []):

        if item["country"] not in TARGET_COUNTRIES:
            continue

        events.append({
            "source": "WOAH",
            "report_id": item["reportId"],
            "event_id": item["eventId"],
            "country": item["country"],
            "disease": item["disease"],
            "report_type": item["reportType"],
            "status": item["eventStatus"],
            "submission_date": item["submissionDate"]
        })

    return events
