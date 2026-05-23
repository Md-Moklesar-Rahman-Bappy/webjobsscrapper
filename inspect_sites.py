"""Inspect all 6 new job sites the user wants to add"""
import sys, json
from playwright.sync_api import sync_playwright

sites = [
    {"name": "WelcomeToTheJungle", "url": "https://app.welcometothejungle.com/en/jobs?query=golang&remote=remote", "login_url": "https://app.welcometothejungle.com/auth/sign-in"},
    {"name": "BuiltIn", "url": "https://builtin.com/jobs?search=golang&remote=all", "login_url": "https://builtin.com/login"},
    {"name": "Workable", "url": "https://jobs.workable.com/search?keywords=golang&remote=on", "login_url": "https://jobs.workable.com/login"},
    {"name": "Greenhouse", "url": "https://my.greenhouse.io/", "note": "ATS portal, not a job board"},
    {"name": "HiringCafe", "url": "https://hiring.cafe/search?q=golang", "login_url": "https://hiring.cafe/login"},
    {"name": "EuRemoteJobs", "url": "https://euremotejobs.com/?s=golang", "login_note": "No login needed"},
]

with sync_playwright() as pw:
    browser = pw.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1920, "height": 1080})
    
    for site in sites:
        print(f"\n{'='*60}")
        print(f"Site: {site['name']}")
        print(f"URL: {site['url']}")
        print(f"{'='*60}")
        
        try:
            page.goto(site['url'], wait_until="domcontentloaded", timeout=15000)
            html = page.content()
            
            # Check for common job elements
            selectors_to_check = [
                "h2", "h3", 
                "a[href*='job']", "a[href*='position']",
                "[class*=job]", "[class*=card]", "[class*=result]",
                "[class*=listing]", "[class*=offer]", 
                "article", "[role='listitem']", "li",
                "div[class*=Job]", "div[class*=SearchResult]",
            ]
            
            found_any = False
            for sel in selectors_to_check:
                els = page.query_selector_all(sel)
                if els:
                    # Filter to elements that contain job-like text
                    real_jobs = []
                    for el in els[:15]:
                        text = (el.inner_text() or "").strip()[:100]
                        if text and len(text) > 10 and ('golang' in text.lower() or 'go' in text.lower().split()):
                            href = ""
                            try:
                                href = el.get_attribute("href") or ""
                            except:
                                pass
                            real_jobs.append((text, href[:80]))
                    
                    if real_jobs:
                        found_any = True
                        print(f"\n  Selector '{sel}':")
                        for text, href in real_jobs[:5]:
                            print(f"    '{text}'")
                            if href:
                                print(f"    -> {href}")
            
            if not found_any:
                print(f"  No job elements found with common selectors")
                # Show all clickable elements that might be jobs
                print(f"\n  Page title: {page.title()[:100]}")
                # Check login link
                login_links = page.query_selector_all("a[href*='login'], a[href*='sign-in']")
                if login_links:
                    print(f"  Login links found: {len(login_links)}")
                else:
                    print(f"  No login links found")
                    
        except Exception as e:
            print(f"  Error: {e}")
        
        print()
    
    browser.close()
