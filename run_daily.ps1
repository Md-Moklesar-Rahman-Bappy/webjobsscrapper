param(
    [switch]$OpenBrowser
)

$ErrorActionPreference = "Continue"
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location -LiteralPath $scriptPath

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Go/AI Remote Job Finder - Daily Run" -ForegroundColor Cyan
Write-Host "  $(Get-Date -Format 'yyyy-MM-dd HH:mm')" -ForegroundColor White
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$logDir = Join-Path -Path $scriptPath -ChildPath "logs"
if (-not (Test-Path -LiteralPath $logDir)) {
    New-Item -ItemType Directory -Path $logDir -Force | Out-Null
}
$logFile = Join-Path -Path $logDir -ChildPath "run_$(Get-Date -Format 'yyyy-MM-dd').log"

# Load .env if it exists
$envFile = Join-Path -Path $scriptPath -ChildPath ".env"
if (Test-Path -LiteralPath $envFile) {
    Write-Host "[INFO] Loading credentials from .env file..." -ForegroundColor Yellow
    Get-Content $envFile | ForEach-Object {
        if ($_ -match "^\s*([A-Z_]+)=(.*)$") {
            [Environment]::SetEnvironmentVariable($matches[1], $matches[2])
        }
    }
    Write-Host "[INFO] Credentials loaded" -ForegroundColor Green
} else {
    Write-Host "[WARN] No .env file found. Copy .env.example to .env and add your logins." -ForegroundColor Red
    Write-Host "       Copy-Item .env.example .env" -ForegroundColor Gray
}

# Check for LinkedIn credentials
$linkedInEmail = [Environment]::GetEnvironmentVariable("LINKEDIN_EMAIL")
if ($linkedInEmail) {
    Write-Host "[INFO] LinkedIn credentials configured for: $linkedInEmail" -ForegroundColor Green
} else {
    Write-Host "[WARN] LinkedIn not configured - will skip logged-in scraping" -ForegroundColor Yellow
}

# Run the scraper
Write-Host "`n[1/2] Running job scraper..." -ForegroundColor Yellow
python scraper.py 2>&1 | ForEach-Object { $_; $_ | Out-File -FilePath $logFile -Append }

# Generate curated list
Write-Host "`n[2/2] Generating curated job CSV..." -ForegroundColor Yellow
python generate_joblist.py 2>&1 | ForEach-Object { $_; $_ | Out-File -FilePath $logFile -Append }

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Done!" -ForegroundColor Green
Write-Host "  Log: $logFile" -ForegroundColor Gray

$csvFile = Join-Path -Path $scriptPath -ChildPath "output" | Join-Path -ChildPath "jobs_$(Get-Date -Format 'yyyy-MM-dd').csv"
Write-Host "  CSV: $csvFile" -ForegroundColor Gray

Write-Host "`n=== QUICK COMMANDS ===" -ForegroundColor Magenta
Write-Host "  Open CSV:       Start-Process '$csvFile'" -ForegroundColor White
Write-Host "  Open job tabs:  .\open_job_searches.ps1" -ForegroundColor White
Write-Host "  Update config:  notepad sources_config.json" -ForegroundColor White
Write-Host "  Add login:      notepad .env" -ForegroundColor White
Write-Host "========================================" -ForegroundColor Cyan

if ($OpenBrowser) {
    Write-Host "`nOpening job search tabs..." -ForegroundColor Yellow
    & ".\open_job_searches.ps1"
}
