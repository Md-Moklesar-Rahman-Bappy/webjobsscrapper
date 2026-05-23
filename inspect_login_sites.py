"""Deep inspect sites that need login"""
from playwright.sync_api import sync_playwright

creds = [
    {"name": "WelcomeToTheJungle", 
     "url": "https://app.welcometothejungle.com/en/jobs?query=golang&remote=remote",
     "login_url": "https://app.welcometothejungle.com/auth/sign-in",
     "email": "ronluke11652@gmail.com",
     "pass": "Sm@rtlee0208!!"},
    {"name": "BuiltIn",
     "url": "https://builtin.com/jobs?search=golang&remote=all",
     "login_url": "https://builtin.com/login",
     "email": "ronluke11652@gmail.com",
     "pass": "Sm@rtlee0208!!"},
    {"name": "HiringCafe",
     "url": "https://hiring.cafe/search?q=golang",
     "login_url": "https://hiring.cafe/login",
     "email": "ronluke11652@gmail.com",
     "pass": "Sm@rtlee0208!!"},
    {"name": "Workable",
     "url": "https://jobs.workable.com/search?keywords=golang&remote=on",
     "email": "ronluke11652@gmail.com",
     "pass": "Sm@rtlee0208!!"},
    {"name": "EuRemoteJobs",
     "url": "https://euremotejobs.com/?s=golang",
     "note": "No login needed, already inspected"},
]

with sync_playwright() as pw:
    browser = pw.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1920, "height": 1080})
    
    for site in creds:
        print(f"\n{'='*60}")
        print(f"Site: {site['name']}")
        print(f"{'='*60}")
        
        try:
            # First check login page fields
            if "login_url" in site:
                print(f"\n[Inspecting login page: {site['login_url']}]")
                page.goto(site["login_url"], wait_until="domcontentloaded", timeout=15000)
                
                # Find email/password fields
                for sel in ["input[type='email']", "input[name='email']", "input[id*='email']", 
                           "input[type='text']", "input[name='login']", "input[id*='login']",
                           "input[autocomplete='email']", "input[id*='username']"]:
                    els = page.query_selector_all(sel)
                    for el in els:
                        ph = el.get_attribute("placeholder") or ""
                        name = el.get_attribute("name") or ""
                        fid = el.get_attribute("id") or ""
                        if ph or name or fid:
                            print(f"  Email field: selector='{sel}', placeholder='{ph}', name='{name}', id='{fid}'")
                
                for sel in ["input[type='password']", "input[name='password']", "input[id*='password']",
                           "input[autocomplete='current-password']"]:
                    els = page.query_selector_all(sel)
                    for el in els:
                        ph = el.get_attribute("placeholder") or ""
                        name = el.get_attribute("name") or ""
                        fid = el.get_attribute("id") or ""
                        if ph or name or fid:
                            print(f"  Password field: selector='{sel}', placeholder='{ph}', name='{name}', id='{fid}'")
                
                for sel in ["button[type='submit']", "button:has-text('Sign')", "button:has-text('Log')",
                           "button:has-text('Continue')", "input[type='submit']", "button:has-text('Se connecter')"]:
                    btns = page.query_selector_all(sel)
                    for btn in btns:
                        txt = btn.inner_text()[:50]
                        print(f"  Submit button: selector='{sel}', text='{txt}'")
            
            # Now try logging in and checking job page
            if "email" in site and site.get("email"):
                print(f"\n[Attempting login + job search]")
                # Fill login
                email_sel = page.query_selector("input[type='email'], input[name='email'], input[id*='email'], input[type='text']")
                pass_sel = page.query_selector("input[type='password'], input[name='password'], input[id*='password']")
                btn_sel = page.query_selector("button[type='submit'], button:has-text('Sign'), button:has-text('Log'), button:has-text('Continue')")
                
                if email_sel and pass_sel:
                    email_sel.fill(site["email"])
                    pass_sel.fill(site["pass"])
                    if btn_sel:
                        btn_sel.click()
                        page.wait_for_timeout(3000)
                        print(f"  After login, URL: {page.url[:120]}")
                        
                        # Now go to job search
                        page.goto(site["url"], wait_until="domcontentloaded", timeout=15000)
                        page.wait_for_timeout(2000)
                        print(f"  Job page URL: {page.url[:120]}")
                        print(f"  Page title: {page.title()[:100]}")
                        
                        # Find job elements
                        for sel in ["h2", "h3", "article", "[class*=job]", "[class*=card]", 
                                   "[class*=result]", "a[href*='job']", "[role='listitem']",
                                   "li", "div[class*=Job]"]:
                            els = page.query_selector_all(sel)
                            if els:
                                # Check first few for job content
                                job_count = 0
                                for el in els[:20]:
                                    text = (el.inner_text() or "").strip()[:80]
                                    if text and len(text) > 10:
                                        job_count += 1
                                if job_count > 2:
                                    print(f"  Selector '{sel}': {job_count} elements (sample: {(els[0].inner_text() or '')[:60]})")
                else:
                    print(f"  Could not find login fields. Email_sel={email_sel}, Pass_sel={pass_sel}")
                    
        except Exception as e:
            print(f"  Error: {e}")
    
    browser.close()
