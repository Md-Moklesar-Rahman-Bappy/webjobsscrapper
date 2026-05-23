import requests
from bs4 import BeautifulSoup

url = "https://euremotejobs.com/?s=golang"
headers = {"User-Agent": "Mozilla/5.0"}
resp = requests.get(url, headers=headers, timeout=30)
soup = BeautifulSoup(resp.text, "html.parser")
# Print all class names from divs
divs = soup.find_all("div", class_=True)
classes = set()
for d in divs:
    for c in d.get("class", []):
        classes.add(c)
print("All div classes:")
for c in sorted(classes):
    print(f"  .{c}")

# Print h2/h3 tags
headers = soup.find_all(["h2", "h3"])
print(f"\nFound {len(headers)} h2/h3 tags:")
for h in headers[:10]:
    print(f"  {h.name}: {h.get_text(strip=True)[:80]}")

# Print all links with 'golang' or 'go' in text
links = soup.find_all("a")
print(f"\nTotal links: {len(links)}")
for l in links[:20]:
    text = l.get_text(strip=True)
    href = l.get("href", "")
    if text and len(text) > 10:
        print(f"  {text[:60]} -> {href[:80]}")
