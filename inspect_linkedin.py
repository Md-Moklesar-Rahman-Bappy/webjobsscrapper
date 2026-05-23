from playwright.sync_api import sync_playwright

with sync_playwright() as pw:
    browser = pw.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1280, "height": 800})
    page.goto("https://www.linkedin.com/login", wait_until="domcontentloaded", timeout=30000)
    page.wait_for_timeout(3000)
    # Print all input fields
    inputs = page.query_selector_all("input")
    print(f"Found {len(inputs)} input fields:")
    for inp in inputs:
        name = inp.get_attribute("name") or ""
        id_ = inp.get_attribute("id") or ""
        type_ = inp.get_attribute("type") or ""
        placeholder = inp.get_attribute("placeholder") or ""
        print(f"  name={name:20s} id={id_:20s} type={type_:10s} placeholder={placeholder}")
    
    # Print all buttons
    buttons = page.query_selector_all("button")
    print(f"\nFound {len(buttons)} buttons:")
    for btn in buttons:
        type_ = btn.get_attribute("type") or ""
        text = btn.inner_text()[:40] if btn.inner_text() else ""
        print(f"  type={type_:15s} text={text}")
    
    browser.close()
