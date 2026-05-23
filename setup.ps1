param(
    [switch]$Full
)

$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location -LiteralPath $scriptPath

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Go/AI Remote Job Finder - Setup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Install Python dependencies
Write-Host "[1/4] Installing Python dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt 2>&1 | Out-Null
Write-Host "  Done" -ForegroundColor Green

# Step 2: Install Playwright browser
Write-Host "[2/4] Installing Playwright Chromium browser..." -ForegroundColor Yellow
python -m playwright install chromium 2>&1 | Out-Null
Write-Host "  Done" -ForegroundColor Green

# Step 3: Create .env from example if not exists
Write-Host "[3/4] Setting up credentials..." -ForegroundColor Yellow
$envFile = Join-Path -Path $scriptPath -ChildPath ".env"
$envExample = Join-Path -Path $scriptPath -ChildPath ".env.example"
if (-not (Test-Path -LiteralPath $envFile)) {
    Copy-Item -Path $envExample -Destination $envFile
    Write-Host "  Created .env file from .env.example" -ForegroundColor Green
    Write-Host "  EDIT IT with your credentials: notepad .env" -ForegroundColor Yellow
} else {
    Write-Host "  .env file already exists" -ForegroundColor Green
}

# Step 4: Create directories
Write-Host "[4/4] Creating directories..." -ForegroundColor Yellow
$dirs = @("output", "data", "logs")
foreach ($d in $dirs) {
    $path = Join-Path -Path $scriptPath -ChildPath $d
    if (-not (Test-Path -LiteralPath $path)) {
        New-Item -ItemType Directory -Path $path -Force | Out-Null
    }
}
Write-Host "  Done" -ForegroundColor Green

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Setup Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "NEXT STEPS:" -ForegroundColor Magenta
Write-Host "  1. Add your LinkedIn login:   notepad .env" -ForegroundColor White
Write-Host "  2. (Optional) Add more sites:  notepad sources_config.json" -ForegroundColor White
Write-Host "  3. Run daily scraper:         .\run_daily.ps1" -ForegroundColor White
Write-Host "  4. Open job browser tabs:     .\open_job_searches.ps1" -ForegroundColor White
Write-Host ""
Write-Host "HOW TO ADD A NEW WEBSITE:" -ForegroundColor Magenta
Write-Host "  Edit sources_config.json and add a new entry like:" -ForegroundColor White
Write-Host '  { "name": "MySite", "enabled": true, "method": "http", "url": "..." }' -ForegroundColor Gray
Write-Host "  See the existing entries for examples of all fields." -ForegroundColor Gray
Write-Host ""
Write-Host "SCHEDULE DAILY (8 AM):" -ForegroundColor Magenta
Write-Host "  Open Task Scheduler -> Create Basic Task" -ForegroundColor White
Write-Host "  Action: Start a program" -ForegroundColor Gray
Write-Host '  Program: powershell.exe' -ForegroundColor Gray
Write-Host '  Arguments: -ExecutionPolicy Bypass -File "'$scriptPath'\run_daily.ps1"' -ForegroundColor Gray
Write-Host "  Trigger: Daily at 8:00 AM" -ForegroundColor Gray

if ($Full) {
    Write-Host ""
    Write-Host "Opening sources_config.json for editing..." -ForegroundColor Yellow
    notepad (Join-Path -Path $scriptPath -ChildPath "sources_config.json")
}
