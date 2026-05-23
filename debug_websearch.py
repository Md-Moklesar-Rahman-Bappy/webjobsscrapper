from duckduckgo_search import DDGS

# Test a single query and print raw results
q = 'site:linkedin.com/jobs "golang" remote'
results = DDGS().text(q, max_results=10, region="wt-wt", safesearch="off", timelimit="w")
print(f"Query: {q}")
print(f"Results: {len(results)}")
for r in results:
    print(f"\nTitle: {r.get('title','')}")
    print(f"  URL: {r.get('href','')}")
    print(f"  Body: {r.get('body','')[:150]}")
    print(f"  Has 'job': {'job' in r.get('title','').lower() or 'job' in r.get('body','').lower()}")
    print(f"  Has 'golang': {'golang' in r.get('title','').lower() or 'golang' in r.get('body','').lower()}")
