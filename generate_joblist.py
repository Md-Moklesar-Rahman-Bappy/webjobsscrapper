import csv, os
from datetime import datetime

output_dir = "output"
os.makedirs(output_dir, exist_ok=True)

today = datetime.now().strftime("%Y-%m-%d")
csv_path = os.path.join(output_dir, f"jobs_{today}.csv")

jobs = [
    # (Company, Title, Link, Salary, Source)
    ("Decision Foundry", "Sr Software Engineer - AI Developer Tools", "https://jaabz.com/jobs/188014-senior-software-engineer-ai-developer-tools", "$184K-$260K", "Jaabz"),
    ("La Fosse / Prediction Markets", "Backend Engineer (Go) for Prediction Markets", "https://jaabz.com/jobs/214815-backend-engineer-go-predictive-markets-fully-remote", "Competitive + Equity", "Jaabz"),
    ("Salesforge", "Senior Backend Engineer - Build AI Agents", "https://www.golangprojects.com/golang-remote-job-gmk-Remote-Europe-Senior-Backend-Engineer-Build-AI-Agents-Salesforge-remotejob.html", "Competitive", "GolangProjects"),
    ("Cast AI", "Senior Software Engineer (Go)", "https://www.golangprojects.com/golang-remote-jobs.html", "78K-108K EUR", "GolangProjects"),
    ("HelloFresh (via Intellias)", "Senior Golang Engineer", "https://career.intellias.com/vacancy/senior-golang-engineer-29990/", "Competitive", "Intellias"),
    ("HelloFresh (via Intellias)", "Senior Golang Engineer", "https://career.intellias.com/vacancy/senior-golang-engineer-29859/", "Competitive", "Intellias"),
    ("Intellias", "Senior Go Engineer with Kubernetes", "https://career.intellias.com/vacancy/senior-go-engineer-with-kubernetes-skills-29943/", "Competitive", "Intellias"),
    ("Mitek Systems", "Senior Software Engineer - Golang and AWS Microservices", "https://workinvirtual.com/job/senior-software-engineer-cloud-platform-golang-aws-microservices/", "Competitive", "WorkinVirtual"),
    ("SmartBrain.io", "Senior Golang Backend Developer (Docker SQL/NoSQL)", "https://smartbrain.io/jobs/project/senior-golang-backend-developer-docker-sqlnosql/b94MWzV", "Competitive", "SmartBrain"),
    ("SmartBrain.io", "Senior Golang Developer (Microservices GraphQL gRPC)", "https://smartbrain.io/jobs/project/senior-golang-developer-microservices-graphql-grpc/mVXYyOE", "Competitive", "SmartBrain"),
    ("Lucenia", "Senior Software Engineer (Go) - Control Plane", "https://hireza.wuaze.com/job/remote-senior-software-engineer-go-control-plane", "Competitive", "Hireza"),
    ("Better (Fintech)", "Middle Golang Developer (Backend/Platform)", "https://hireza.wuaze.com/job/remote-middle-golang-developer-backend-platform-2", "Competitive", "Hireza"),
    ("LaunchDarkly-like", "Backend Engineer - Mid-Senior Level (Golang)", "https://hireza.wuaze.com/job/backend-engineer-mid-senior-level-golang", "$127K-$204K + RSU", "Hireza"),
    ("PerfectScale by DoiT", "Senior Backend Engineer (Golang)", "https://hireza.wuaze.com/job/senior-backend-engineergolang-perfectscale-by-doit-3", "Competitive", "Hireza"),
    ("WebSenor", "Golang + Node.js Developer", "https://websenor.com/jobs/golang-node-js-developer-2/", "Competitive", "WebSenor"),
    ("Ruby Labs", "Middle Golang Developer", "https://hirequill.liveblog365.com/job/golang-developer-3", "Competitive", "Hirequill"),
    ("G2I Inc.", "Go Software Engineer AI", "https://anywhereremotejobs.com/remote-jobs/go-software-engineer-ai-at-g2i-a31f2c55", "$30-$70/hr", "AnywhereRemote"),
    ("Turing", "Software Engineer - Agentic AI Data Cloud (Python/Go)", "https://www.remotejobleads.com/software-engineer-agentic-ai-data-cloud-python-go-2/", "$49-$70/hr", "RemoteJobLeads"),
    ("Blau Direkt", "AI / LLM Software Engineer (Go)", "https://nofluffjobs.com/job/ai-llm-software-engineer-blau-direkt-poland-remote", "Competitive", "NoFluffJobs"),
    ("CodiLime", "Mid/Senior Go Engineer with Web API experience", "https://nofluffjobs.com/job/mid-senior-go-engineer-with-web-api-experience-codilime-remote", "Competitive", "NoFluffJobs"),
    ("DCG Sp. z o.o.", "Senior Golang Developer", "https://nofluffjobs.com/job/senior-golang-developer-dcg-remote", "~$8K/mo B2B", "NoFluffJobs"),
    ("From Poland With Dev", "Senior Golang Engineer (Payment solutions)", "https://nofluffjobs.com/job/senior-golang-engineer-us-product-payment-solutions-from-poland-with-dev-subcarpathian", "~$7K/mo B2B", "NoFluffJobs"),
    ("Makeitright", "Golang Developer (Kubernetes)", "https://nofluffjobs.com/job/golang-developer-kubernetes-makeitright-remote-1", "~$6K/mo B2B", "NoFluffJobs"),
    ("Donfod / USA", "Go Developer", "https://donfod.com/2026/05/01/go-developer-remote-full-time/", "$115K-$180K", "Donfod"),
    ("IDT Corporation", "Senior Golang Software Engineer", "https://rs.linkedin.com/jobs/view/senior-golang-software-engineer-n2p-at-idt-corporation-4184830600", "Competitive", "LinkedIn"),
    ("Tyk (via Lynn News)", "Senior Go Developer", "https://uk.linkedin.com/jobs/view/senior-go-developer-at-lynn-news-4250966680", "Competitive", "LinkedIn"),
    ("uDelta", "Senior Software Developer (Go)", "https://rs.linkedin.com/jobs/view/senior-software-developer-go-at-udelta-4190253944", "Competitive", "LinkedIn"),
    ("OLX", "Senior Software Engineer (Golang) - Remote Poland", "https://pl.linkedin.com/jobs/view/senior-software-engineer-golang-java-php-remote-within-poland-at-olx-4137532355", "Competitive", "LinkedIn"),
    ("Call For Referral", "Sr SWE Distributed Systems and Go", "https://ee.linkedin.com/jobs/view/senior-software-engineer-distributed-systems-go-24200k-24300k-remote-europe-at-call-for-referral-4031826138", "$200K-$300K", "LinkedIn"),
    ("Brixio", "Senior Golang Developer", "https://ph.linkedin.com/jobs/view/senior-golang-developer-at-brixio-4170790106", "Competitive", "LinkedIn"),
    ("AUTODOC", "Senior Golang Developer", "https://www.linkedin.com/jobs/view/senior-golang-developer-at-autodoc-4160238190", "Competitive", "LinkedIn"),
    ("NARD POS", "Senior Golang Developer", "https://jo.linkedin.com/jobs/view/senior-golang-developer-at-nard-pos-4148244657", "Competitive", "LinkedIn"),
    ("Kubegrade", "Senior Go Developer (remote)", "https://th.linkedin.com/jobs/view/senior-go-developer-remote-at-kubegrade-4132060872", "Competitive", "LinkedIn"),
    ("Professional.me", "Remote Golang Developer", "https://ua.linkedin.com/jobs/view/remote-golang-developer-at-professional-me-4153831727", "Competitive", "LinkedIn"),
    ("GRAX Inc", "Senior Golang Full Stack Developer", "https://www.golangprojects.com/golang-remote-jobs.html", "$150K-$180K", "GolangProjects"),
    ("Voodoo", "Staff Backend Engineer - Golang", "https://www.golangprojects.com/golang-remote-jobs.html", "Competitive", "GolangProjects"),
    ("Group-IB", "Senior Golang Developer", "https://www.golangprojects.com/golang-remote-jobs.html", "Competitive", "GolangProjects"),
    ("CYZA", "Backend Go Engineer", "https://www.golangprojects.com/golang-remote-jobs.html", "Competitive", "GolangProjects"),
    ("TRE ALTAMIRA Srl", "Senior Golang Developer", "https://www.golangprojects.com/golang-remote-jobs.html", "50K-65K EUR", "GolangProjects"),
]

with open(csv_path, "w", newline="", encoding="utf-8-sig") as f:
    w = csv.writer(f)
    w.writerow(["Company", "Title", "Link", "Salary", "Source", "Notes"])
    for company, title, link, salary, source in jobs:
        notes = ""
        if "AI" in title or "AI" in company:
            notes = "AI-related role"
        elif "Senior" in title:
            notes = "Senior role - matches experience"
        w.writerow([company, title, link, salary, source, notes])

print(f"Saved {len(jobs)} jobs to {csv_path}")
print(f"\nTop matches for your profile (Senior Golang, 10yr exp, AI/Go):")
print(f"{'='*60}")
for company, title, link, salary, source in jobs:
    score = 0
    title_lower = title.lower()
    if "senior" in title_lower: score += 5
    if "golang" in title_lower or "go " in title_lower or " go" in title_lower: score += 5
    if any(kw in title_lower for kw in ["ai", "engineer", "backend", "distributed", "kubernetes", "aws"]): score += 3
    if score >= 10:
        print(f"\n  [{score}pts] {company} - {title}")
        print(f"    {salary}")
        print(f"    {link}")
