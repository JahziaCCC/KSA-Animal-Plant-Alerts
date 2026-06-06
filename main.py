import os
import requests

TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

message = """
🧪 رسالة اختبار

تم تشغيل KSA Animal & Plant Alerts بنجاح.
"""

url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

requests.post(
    url,
    json={
        "chat_id": CHAT_ID,
        "text": message
    }
)
