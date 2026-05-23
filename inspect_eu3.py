import requests
from bs4 import BeautifulSoup

url = "https://euremotejobs.com/?s=golang"
headers = {"User-Agent": "Mozilla/5.0"}
resp = requests.get(url, headers=headers, timeout=30)
soup = BeautifulSoup(resp.text, "html.parser")
# Find the actual structure - print all element types
for i, el in enumerate(soup.find_all(True, limit=100)):
    if el.name in ["article", "div", "section", "li", "ul"] and el.get("class"):
        print(f"{i:4d} <{el.name} class={el.get('class')}> -> {el.get_text(strip=True)[:80]}")
    elif el.name in ["h1", "h2", "h3", "h4"]:
        print(f"{i:4d} <{el.name}> {el.get_text(strip=True)[:80]}")
    elif el.name == "a" and el.get("href"):
        text = el.get_text(strip=True)
        href = el.get("href", "")
        if text and len(text) > 5:
            print(f"{i:4d} <a> '{text[:50]}' -> {href[:60]}")
