Write-Host "=== Opening Job Search Pages in Browser ===" -ForegroundColor Cyan
Write-Host "This will open multiple tabs with Go remote job searches.`n" -ForegroundColor Yellow

$searches = @(
    "https://www.linkedin.com/jobs/search/?keywords=golang%20remote&f_WT=2&f_TPR=r604800&geoId=92000000",
    "https://www.linkedin.com/jobs/search/?keywords=go%20engineer%20remote&f_WT=2&f_TPR=r604800",
    "https://www.indeed.com/jobs?q=golang+remote&fromage=7&sort=date",
    "https://www.indeed.com/jobs?q=go+developer+remote&fromage=7&sort=date",
    "https://weworkremotely.com/remote-jobs/search?term=golang",
    "https://remoteok.com/remote-golang-jobs",
    "https://www.golangprojects.com/golang-remote-jobs.html",
    "https://stackoverflow.com/jobs?q=golang+remote&r=true",
    "https://www.simplyhired.com/search?q=golang+remote&fdb=7",
    "https://www.glassdoor.com/Job/jobs.htm?sc.keyword=golang+remote&fromAge=7",
    "https://www.ziprecruiter.com/candidate/search?search=golang&remote=1&days=7",
    "https://remotive.com/remote-jobs/software-dev/golang",
    "https://jobicy.com/jobs/?s=golang&remote=true",
    "https://www.upwork.com/search/jobs/?q=golang&contract_type=any&workload=any",
)

foreach ($url in $searches) {
    Write-Host "Opening: $url" -ForegroundColor Gray
    Start-Process $url
    Start-Sleep -Milliseconds 300
}

Write-Host "`nDone! $($searches.Count) tabs opened." -ForegroundColor Green
Write-Host "Quick Tip: Apply filters for 'Past Week' on each site." -ForegroundColor Yellow
