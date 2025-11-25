@echo off
echo ========================================
echo   Push to GitHub - Quick Script
echo ========================================
echo.

echo Checking git status...
git status
echo.

echo ========================================
echo Ready to push all changes to GitHub?
echo Repository: https://github.com/dhirajkk91/Face-and-Object-tracking
echo ========================================
echo.
pause

echo.
echo Adding all files...
git add .

echo.
echo Committing changes...
git commit -m "Add comprehensive documentation and improve codebase structure - Added detailed docstrings to all Python modules - Enhanced README with complete feature list - Created CONTRIBUTING.md and LICENSE - Improved code documentation and comments - Added utility scripts and guides"

echo.
echo Pushing to GitHub...
git push origin main

echo.
echo ========================================
if %ERRORLEVEL% EQU 0 (
    echo SUCCESS! Changes pushed to GitHub
    echo Visit: https://github.com/dhirajkk91/Face-and-Object-tracking
) else (
    echo.
    echo Push failed. Trying 'master' branch...
    git push origin master
    if %ERRORLEVEL% EQU 0 (
        echo SUCCESS! Changes pushed to GitHub
        echo Visit: https://github.com/dhirajkk91/Face-and-Object-tracking
    ) else (
        echo.
        echo ERROR: Push failed. Please check:
        echo 1. Internet connection
        echo 2. GitHub authentication
        echo 3. Branch name (main or master^)
        echo.
        echo See GITHUB_PUSH_GUIDE.md for help
    )
)
echo ========================================
echo.
pause
