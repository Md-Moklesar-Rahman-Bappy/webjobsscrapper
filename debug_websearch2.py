from duckduckgo_search import DDGS

# Test broader queries without site:
queries = [
    '"golang" "engineer" remote',
    '"golang" remote job senior',
    '"go" "backend" engineer remote',
    'golang developer remote hiring',
]

for q in queries:
    results = DDGS().text(q, max_results=10, region="wt-wt", safesearch="off", timelimit="w")
    print(f"\nQuery: {q}")
    print(f"Results: {len(results)}")
    for r in results[:3]:
        print(f"  Title: {r.get('title','')[:80]}")
        print(f"  URL: {r.get('href','')[:80]}")
        print(f"  Body: {r.get('body','')[:100]}")
