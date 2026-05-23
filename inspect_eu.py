import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import requests
from bs4 import BeautifulSoup

url = "https://euremotejobs.com/?s=golang"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
resp = requests.get(url, headers=headers, timeout=30)
soup = BeautifulSoup(resp.text, "html.parser")
articles = soup.select("article")
print(f"Found {len(articles)} articles")
for a in articles[:3]:
    print(f"\n--- Article HTML ---")
    print(a.prettify()[:800])
