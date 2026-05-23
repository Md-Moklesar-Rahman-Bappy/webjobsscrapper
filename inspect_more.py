"""Check BuiltIn login form fields and WTTJ job listing"""
from playwright.sync_api import sync_playwright

with sync_playwright() as pw:
    browser = pw.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1920, "height": 1080})

    # === BuiltIn Login ===
    print("="*60)
    print("BuiltIn - login form fields")
    print("="*60)
    page.goto("https://builtin.com/login", wait_until="domcontentloaded", timeout=15000)
    page.wait_for_timeout(2000)
    print(f"URL: {page.url[:140]}")
    
    # List ALL input fields
    inputs = page.query_selector_all("input")
    print(f"\nAll input fields: {len(inputs)}")
    for inp in inputs:
        typ = inp.get_attribute("type") or ""
        name = inp.get_attribute("name") or ""
        pid = inp.get_attribute("id") or ""
        ph = inp.get_attribute("placeholder") or ""
        cl = (inp.get_attribute("class") or "")[:60]
        print(f"  type='{typ}' name='{name}' id='{pid}' placeholder='{ph}' class='{cl}'")
    
    # Find submit button
    buttons = page.query_selector_all("button, input[type='submit']")
    print(f"\nSubmit buttons: {len(buttons)}")
    for btn in buttons:
        txt = (btn.inner_text() or btn.get_attribute("value") or "")[:80]
        typ = btn.get_attribute("type") or ""
        print(f"  type='{typ}' text='{txt}'")

    # Try BuiltIn job search without login 
    print(f"\n{'='*60}")
    print("BuiltIn - job search page (no login)")
    print("="*60)
    page.goto("https://builtin.com/jobs?search=golang&remote=all", wait_until="domcontentloaded", timeout=15000)
    page.wait_for_timeout(3000)
    print(f"URL: {page.url[:150]}")
    print(f"Title: {page.title()[:100]}")
    
    for _ in range(3):
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        page.wait_for_timeout(1000)
    
    for sel in ["article", "div[class*=job]", "h2", "h3", "a[href*='/job/']",
                "[class*=card]", "li[class*=job]", "section[class*=job]"]:
        els = page.query_selector_all(sel)
        if els:
            relevant = []
            for el in els:
                text = (el.inner_text() or "").strip()
                if text and len(text) > 20:
                    relevant.append(text[:80])
            if relevant:
                print(f"\nSelector '{sel}': {len(relevant)} relevant")
                for r in relevant[:3]:
                    print(f"  '{r}'")

    # === WTTJ - try different search URL ===
    print(f"\n{'='*60}")
    print("WTTJ - check search page after fresh login")
    print("="*60)
    page.goto("https://app.welcometothejungle.com/auth/sign-in", wait_until="domcontentloaded", timeout=15000)
    page.fill("input[name='email']", "ronluke11652@gmail.com")
    page.fill("input[name='password']", "Sm@rtlee0208!!")
    page.click("button[type='submit']")
    page.wait_for_timeout(3000)
    
    # Try going directly to search with query params
    page.goto("https://app.welcometothejungle.com/jobs?query=golang", wait_until="domcontentloaded", timeout=15000)
    page.wait_for_timeout(5000)
    print(f"URL: {page.url[:150]}")
    print(f"Title: {page.title()[:100]}")
    
    for _ in range(5):
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        page.wait_for_timeout(1000)
    
    body = page.inner_text("body")
    if "golang" in body.lower():
        print("'golang' found in body!")
    if "remote" in body.lower():
        print("'remote' found in body!")
    
    # Find all job-like links
    links = page.query_selector_all("a")
    job_urls = {}
    for link in links:
        href = link.get_attribute("href") or ""
        text = (link.inner_text() or "").strip()[:80]
        if "/jobs/" in href and len(href.split("/jobs/")[1]) > 5:
            job_id = href.split("/jobs/")[1].split("?")[0]
            if job_id not in job_urls and text:
                job_urls[job_id] = (text, href)
    
    print(f"\nJob URLs found: {len(job_urls)}")
    for jid, (txt, href) in list(job_urls.items())[:10]:
        print(f"  '{txt}' -> {href[:100]}")
    
    browser.close()
