import requests

url = "https://wahis.woah.org/api/v1/pi/event/filtered-list?language=en"

response = requests.get(url, timeout=30)

print(response.status_code)

data = response.json()

print(data["totalSize"])

for item in data["list"][:5]:
    print(item["country"])
    print(item["disease"])
    print("-" * 50)
