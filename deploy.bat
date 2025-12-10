@echo off
echo ============================================
echo Time Management Calculator - Deployment Helper
echo ============================================
echo.

echo This script will help you prepare for deployment.
echo.

echo Step 1: Checking if Git is installed...
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Git is not installed!
    echo Please install Git from: https://git-scm.com/download/win
    echo.
    pause
    exit /b 1
)
echo [OK] Git is installed
echo.

echo Step 2: Do you want to initialize Git repository? (y/n)
set /p init_git="Enter choice: "

if /i "%init_git%"=="y" (
    echo Initializing Git repository...
    git init
    git add .
    git commit -m "Initial commit: Time Management Calculator"
    git branch -M main
    echo.
    echo [OK] Git repository initialized
    echo.
    echo Next steps:
    echo 1. Create a repository on GitHub: https://github.com/new
    echo 2. Run this command with YOUR username:
    echo    git remote add origin https://github.com/YOUR_USERNAME/time-management-calculator.git
    echo 3. Push to GitHub:
    echo    git push -u origin main
    echo.
)

echo Step 3: Backend Deployment
echo ============================================
echo.
echo To deploy your backend to Render.com:
echo 1. Go to https://render.com and sign up
echo 2. Click "New +" -^> "Web Service"
echo 3. Connect your GitHub repository
echo 4. Use these settings:
echo    - Build Command: pip install -r backend/requirements.txt
echo    - Start Command: cd backend ^&^& uvicorn main:app --host 0.0.0.0 --port $PORT
echo    - Plan: Free
echo.
echo After deployment, copy your backend URL (e.g., https://your-app.onrender.com)
echo.

set /p backend_url="Enter your Render backend URL (or press Enter to skip): "

if not "%backend_url%"=="" (
    echo.
    echo Updating frontend API URL...
    
    REM Create a temporary PowerShell script to update the file
    echo $content = Get-Content 'frontend/app.js' -Raw > update_api.ps1
    echo $content = $content -replace "API_URL: 'http://localhost:8000'", "API_URL: '%backend_url%'" >> update_api.ps1
    echo $content ^| Set-Content 'frontend/app.js' >> update_api.ps1
    
    powershell -ExecutionPolicy Bypass -File update_api.ps1
    del update_api.ps1
    
    echo [OK] API URL updated in frontend/app.js
    echo.
    
    if /i "%init_git%"=="y" (
        echo Committing changes...
        git add frontend/app.js
        git commit -m "Update API URL for production"
        echo [OK] Changes committed
        echo Don't forget to push: git push
        echo.
    )
)

echo Step 4: Frontend Deployment
echo ============================================
echo.
echo Choose your frontend hosting option:
echo.
echo Option A - Netlify (Easiest):
echo   1. Go to https://app.netlify.com/drop
echo   2. Drag the 'frontend' folder onto the page
echo   3. Done! Your site is live
echo.
echo Option B - GitHub Pages:
echo   1. Push your code to GitHub (if not done already)
echo   2. Go to repository Settings -^> Pages
echo   3. Select branch 'main' and folder '/frontend'
echo   4. Click Save
echo   5. Wait 2-3 minutes
echo.

echo ============================================
echo Deployment preparation complete!
echo ============================================
echo.
echo Quick Reference:
echo - Backend: Deploy to Render.com using GitHub
echo - Frontend: Deploy to Netlify (drag ^& drop) or GitHub Pages
echo - Full guide: See HOSTING_GUIDE.md
echo.
echo Need help? Check HOSTING_GUIDE.md for detailed instructions.
echo.
pause
