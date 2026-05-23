from sources.engine import scrape_http, load_config

configs = load_config()
print(f"Loaded {len(configs)} sources from config")

for src in configs:
    method = src.get("method", "http")
    print(f"\nSource: {src['name']} (method: {method})")
    if method == "http":
        jobs = scrape_http(src)
        print(f"  -> {len(jobs)} jobs")
        for j in jobs[:3]:
            print(f"     {j['title'][:70]}")
            print(f"     {j['company'][:40]}")
            if j.get("link"):
                print(f"     {j['link'][:80]}")
    else:
        print(f"  (requires Playwright, skipping)")
