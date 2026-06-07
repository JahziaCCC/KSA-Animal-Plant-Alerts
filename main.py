import requests
import json

URL = "https://wahis.woah.org/api/v1/pi/event/filtered-list?language=en"

payload = {
    "animalTypes": [],
    "countries": [],
    "eventIds": [],
    "eventStartDate": None,
    "eventStatuses": [],
    "firstDiseases": [],
    "pageNumber": 0,
    "pageSize": 10,
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

response = requests.post(
    URL,
    json=payload,
    timeout=30
)

print("STATUS:", response.status_code)

data = response.json()

print("TOTAL:", data.get("totalSize"))

print("\nLATEST EVENTS\n")

for item in data.get("list", []):
    print("=" * 60)
    print("Country:", item.get("country"))
    print("Disease:", item.get("disease"))
    print("Report Type:", item.get("reportType"))
    print("Event ID:", item.get("eventId"))
    print("Date:", item.get("submissionDate"))
