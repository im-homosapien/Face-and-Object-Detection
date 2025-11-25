# PowerShell script to install Visual C++ Build Tools and then install dlib
# This script requires Administrator privileges
# Run: powershell -ExecutionPolicy Bypass -File install_dlib.ps1

Write-Host "Installing Visual C++ Build Tools..." -ForegroundColor Green

# Check if running as administrator
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
if (-not $isAdmin) {
    Write-Host "ERROR: This script requires Administrator privileges!" -ForegroundColor Red
    Write-Host "Please run PowerShell as Administrator and try again." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Right-click PowerShell and select 'Run as Administrator'" -ForegroundColor Yellow
    exit 1
}

# Try to install Visual C++ Build Tools using Chocolatey if available
if (Get-Command choco -ErrorAction SilentlyContinue) {
    Write-Host "Using Chocolatey to install Visual C++ Build Tools..." -ForegroundColor Green
    choco install visualstudio2022buildtools -y --params "--quiet --add Microsoft.VisualStudio.Workload.VCTools --includeRecommended"
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Visual C++ Build Tools installed successfully!" -ForegroundColor Green
        Write-Host ""
        Write-Host "Please restart your terminal/command prompt and then run:" -ForegroundColor Yellow
        Write-Host "pip install dlib face-recognition" -ForegroundColor Cyan
    } else {
        Write-Host "Chocolatey installation failed. Please install manually." -ForegroundColor Red
        Write-Host "Download from: https://visualstudio.microsoft.com/downloads/#build-tools-for-visual-studio-2022" -ForegroundColor Yellow
    }
} else {
    Write-Host "Chocolatey not found. Please install Visual C++ Build Tools manually:" -ForegroundColor Yellow
    Write-Host "1. Download from: https://visualstudio.microsoft.com/downloads/#build-tools-for-visual-studio-2022" -ForegroundColor Cyan
    Write-Host "2. Run the installer" -ForegroundColor Cyan
    Write-Host "3. Select 'Desktop development with C++' workload" -ForegroundColor Cyan
    Write-Host "4. After installation, restart your terminal and run: pip install dlib face-recognition" -ForegroundColor Cyan
}

