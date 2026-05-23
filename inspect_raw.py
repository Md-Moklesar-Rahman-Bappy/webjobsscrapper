import requests
from bs4 import BeautifulSoup

url = "https://euremotejobs.com/?s=golang"
headers = {"User-Agent": "Mozilla/5.0"}
resp = requests.get(url, headers=headers, timeout=30)
# Print first 3000 chars
print(resp.text[:3000])
