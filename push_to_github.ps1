# ====================================================================
# PETROCHEMICAL TRADE ANALYTICS - AUTOMATED GITHUB PUSH HELPER
# ====================================================================

param (
    [string]$RepoName = "petrochemical-trade-analytics",
    [string]$RemoteUrl = ""
)

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "   PETROCHEMICAL TRADE ANALYTICS - GITHUB PUSH UTILITY      " -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan

# Check if gh CLI is authenticated
$ghStatus = gh auth status 2>&1

if ($RemoteUrl -ne "") {
    Write-Host "[1/3] Adding remote origin: $RemoteUrl" -ForegroundColor Yellow
    git remote remove origin 2>$null
    git remote add origin $RemoteUrl
    Write-Host "[2/3] Renaming branch to main..." -ForegroundColor Yellow
    git branch -M main
    Write-Host "[3/3] Pushing to remote repository..." -ForegroundColor Green
    git push -u origin main
}
elseif ($ghStatus -match "Logged in to github.com") {
    Write-Host "Detected active GitHub CLI session!" -ForegroundColor Green
    Write-Host "Creating private repository '$RepoName' and pushing code..." -ForegroundColor Yellow
    gh repo create $RepoName --private --source=. --remote=origin --push
    Write-Host "`nSUCCESS! Your project has been pushed to your private GitHub repo." -ForegroundColor Green
}
else {
    Write-Host "`nYou are currently not logged into GitHub CLI on this terminal." -ForegroundColor Yellow
    Write-Host "To link and push your private repository, choose one of these two options:`n" -ForegroundColor White
    
    Write-Host "OPTION A (Recommended - using GitHub CLI):" -ForegroundColor Cyan
    Write-Host "  1. Run: gh auth login" -ForegroundColor White
    Write-Host "     (Select: GitHub.com -> HTTPS -> Yes -> Login with web browser)" -ForegroundColor Gray
    Write-Host "  2. Run: gh repo create $RepoName --private --source=. --remote=origin --push`n" -ForegroundColor White
    
    Write-Host "OPTION B (Using your GitHub Repo URL):" -ForegroundColor Cyan
    Write-Host "  1. Create a new empty private repo on https://github.com/new" -ForegroundColor White
    Write-Host "  2. Run: .\push_to_github.ps1 -RemoteUrl 'https://github.com/<YOUR_USERNAME>/$RepoName.git'" -ForegroundColor White
}
