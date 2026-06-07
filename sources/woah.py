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


def classify_event(report_type, event_status):
    if report_type == "IN":
        return "new_outbreak"

    if report_type == "FUR":
        return "update"

    if str(event_status).lower() == "resolved":
        return "closed"

    return "update"


def fetch_events():
    response = requests.get(URL, timeout=30)
    response.raise_for_status()

    data = response.json()

    events = []

    for item in data.get("list", []):

        country = item.get("country")

        if country not in TARGET_COUNTRIES:
            continue

        events.append({
            "source": "WOAH",
            "report_id": item.get("reportId"),
            "event_id": item.get("eventId"),
            "country": country,
            "disease": item.get("disease"),
            "report_type": item.get("reportType"),
            "event_status": item.get("eventStatus"),
            "submission_date": item.get("submissionDate"),
            "reason": item.get("reason"),
            "category": classify_event(
                item.get("reportType"),
                item.get("eventStatus")
            )
        })

    return events


if __name__ == "__main__":
    events = fetch_events()

    print(f"\nFound {len(events)} matching events\n")

    for event in events:
        print("=" * 80)
        print(event)
