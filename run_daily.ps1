param(
    [switch]$OpenBrowser
)

$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location -LiteralPath $scriptPath

$date = Get-Date -Format "yyyy-MM-dd"
$logDir = Join-Path -Path $scriptPath -ChildPath "logs"
if (-not (Test-Path -LiteralPath $logDir)) {
    New-Item -ItemType Directory -Path $logDir -Force | Out-Null
}

$logFile = Join-Path -Path $logDir -ChildPath "run_$date.log"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Go/AI Remote Job Finder - Daily Run" -ForegroundColor Cyan
Write-Host "  $date" -ForegroundColor White
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Run the scraper (best-effort, adds to DB)
Write-Host "[1/3] Running auto-scraper..." -ForegroundColor Yellow
python scraper.py 2>&1 | Tee-Object -FilePath $logFile

Write-Host ""
Write-Host "[2/3] Generating curated job list..." -ForegroundColor Yellow
python generate_joblist.py 2>&1 | Tee-Object -FilePath $logFile -Append

Write-Host ""
Write-Host "[3/3] Done!" -ForegroundColor Green
Write-Host "Log saved to: $logFile" -ForegroundColor Gray

$csvFile = Join-Path -Path $scriptPath -ChildPath "output" | Join-Path -ChildPath "jobs_$date.csv"
Write-Host "CSV saved to: $csvFile" -ForegroundColor Gray

if ($OpenBrowser) {
    Write-Host ""
    Write-Host "Opening job search pages in browser..." -ForegroundColor Yellow
    & ".\open_job_searches.ps1"
}

Write-Host ""
Write-Host "=== QUICK START ===" -ForegroundColor Magenta
Write-Host "1. Open the CSV: Get-Content '$csvFile'" -ForegroundColor White
Write-Host "2. Or run: .\open_job_searches.ps1  (opens browser tabs)" -ForegroundColor White
Write-Host "3. Or run: python scraper.py  (update DB with web search)" -ForegroundColor White
