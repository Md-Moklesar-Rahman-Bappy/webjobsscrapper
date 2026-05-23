$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location -LiteralPath $scriptPath
$date = Get-Date -Format "yyyy-MM-dd"
$logFile = Join-Path -Path $scriptPath -ChildPath "logs" | Join-Path -ChildPath "run_$date.log"
$logDir = Split-Path -Parent $logFile
if (-not (Test-Path -LiteralPath $logDir)) {
    New-Item -ItemType Directory -Path $logDir -Force | Out-Null
}
python scraper.py 2>&1 | Tee-Object -FilePath $logFile
