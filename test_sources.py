import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from sources.engine import load_config, scrape_http

configs = load_config()
for src in configs:
    if src["name"] == "EuRemoteJobs":
        print(f"Testing {src['name']}...")
        jobs = scrape_http(src)
        print(f"Found {len(jobs)} jobs")
        for j in jobs[:5]:
            print(f"  - {j['title']} @ {j['company']}")
        break
