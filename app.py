import os
import time
import requests
from bs4 import BeautifulSoup

DISCORD_WEBHOOK_URL = os.getenv("WEBHOOK_URL")

URL = "https://trends24.in/japan/"
CHECK_INTERVAL = 300
seen = set()

def get_trends():
    res = requests.get(URL, timeout=10)
    res.encoding = "utf-8"
    soup = BeautifulSoup(res.text, "html.parser")
    trends = soup.select("ol.trend-card__list li")
    return [t.get_text().strip() for t in trends]

def notify(msg):
    requests.post(DISCORD_WEBHOOK_URL, json={"content": msg}, timeout=10)

print("起動")

while True:
    try:
        for text in get_trends():
            if text in seen:
                continue
            if "Rust" in text or "ゲーム" in text:
                notify(f"🔥 {text}")
                seen.add(text)
        time.sleep(CHECK_INTERVAL)
    except Exception as e:
        print(e)
        time.sleep(60)
