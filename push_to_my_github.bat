@echo off
echo ========================================
echo   Push to YOUR GitHub Account
echo   Username: im-homosapien
echo ========================================
echo.

echo STEP 1: Create repository on GitHub first!
echo.
echo Go to: https://github.com/new
echo Repository name: Face-and-Object-Detection
echo Description: Real-time face recognition and object detection system
echo Visibility: Public (or Private)
echo DO NOT initialize with README, .gitignore, or license
echo.
echo Press any key AFTER you've created the repository on GitHub...
pause
echo.

echo ========================================
echo STEP 2: Pushing to your repository...
echo ========================================
echo.

echo Adding any new changes...
git add .

echo.
echo Committing...
git commit -m "Update repository information for im-homosapien account"

echo.
echo Pushing to GitHub...
git push -u origin master

echo.
echo ========================================
if %ERRORLEVEL% EQU 0 (
    echo SUCCESS! Your code is now on GitHub!
    echo.
    echo Visit your repository:
    echo https://github.com/im-homosapien/Face-and-Object-Detection
    echo.
    echo Next steps:
    echo 1. Add topics/tags to your repository
    echo 2. Update the About section
    echo 3. Create a release (v2.0.0^)
    echo 4. Share your work!
) else (
    echo.
    echo Push failed. This might be because:
    echo 1. Repository not created on GitHub yet
    echo 2. Wrong repository name
    echo 3. Authentication needed (use Personal Access Token^)
    echo.
    echo If you used a different repository name, run:
    echo git remote set-url origin https://github.com/im-homosapien/YOUR-REPO-NAME.git
    echo git push -u origin master
)
echo ========================================
echo.
pause
