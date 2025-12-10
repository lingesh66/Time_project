# Deployment Guide for Time Management Calculator

This guide will help you deploy the Time Management Calculator to free hosting services.

## Prerequisites

- GitHub account
- Render.com account (free tier)
- Git installed locally

## Backend Deployment (Render.com)

### Step 1: Push to GitHub

1. Initialize git repository:
```bash
cd d:\Time_project
git init
git add .
git commit -m "Initial commit: Time Management Calculator"
```

2. Create a new repository on GitHub and push:
```bash
git remote add origin https://github.com/YOUR_USERNAME/time-management-calculator.git
git branch -M main
git push -u origin main
```

### Step 2: Deploy to Render

1. Go to [Render.com](https://render.com) and sign up/login
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure the service:
   - **Name**: `time-management-api`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r backend/requirements.txt`
   - **Start Command**: `cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Plan**: Free
5. Click "Create Web Service"
6. Wait for deployment to complete (5-10 minutes)
7. Copy your service URL (e.g., `https://time-management-api.onrender.com`)

**Important**: The project includes a `runtime.txt` file specifying Python 3.11.8. This prevents build errors with newer Python versions. Do not delete this file.

### Step 3: Update Frontend Configuration

1. Open `frontend/app.js`
2. Update the `API_URL` in the CONFIG object:
```javascript
const CONFIG = {
    API_URL: 'https://your-service-name.onrender.com'
};
```
3. Commit and push the changes:
```bash
git add frontend/app.js
git commit -m "Update API URL for production"
git push
```

## Frontend Deployment (GitHub Pages)

### Option 1: Using GitHub Pages

1. Go to your GitHub repository
2. Click "Settings" → "Pages"
3. Under "Source", select:
   - Branch: `main`
   - Folder: `/frontend`
4. Click "Save"
5. Wait a few minutes for deployment
6. Your site will be available at: `https://YOUR_USERNAME.github.io/time-management-calculator/`

### Option 2: Using Netlify

1. Go to [Netlify](https://netlify.com) and sign up/login
2. Click "Add new site" → "Import an existing project"
3. Connect your GitHub repository
4. Configure build settings:
   - **Base directory**: `frontend`
   - **Build command**: (leave empty)
   - **Publish directory**: `.`
5. Click "Deploy site"
6. Your site will be available at a Netlify URL

## Alternative Backend Hosting Options

### Deta Space (Completely Free)

1. Install Deta CLI:
```bash
curl -fsSL https://get.deta.dev/cli.sh | sh
```

2. Login to Deta:
```bash
deta login
```

3. Create a new Deta Space project:
```bash
cd backend
deta new
```

4. Deploy:
```bash
deta deploy
```

### Railway (Free Tier)

1. Go to [Railway.app](https://railway.app)
2. Sign up with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your repository
5. Configure:
   - **Root Directory**: `backend`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
6. Deploy

### Vercel (Serverless)

For serverless deployment, you'll need to modify the backend slightly:

1. Create `backend/vercel.json`:
```json
{
  "builds": [
    {
      "src": "main.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "main.py"
    }
  ]
}
```

2. Deploy:
```bash
cd backend
vercel
```

## Environment Variables

If you need to set environment variables (for future enhancements):

**Render.com:**
- Go to your service → "Environment"
- Add key-value pairs

**Netlify:**
- Go to Site settings → "Environment variables"
- Add variables

## Testing Your Deployment

1. Visit your frontend URL
2. Click "Load Sample" to load test data
3. Click "Calculate Logout Time"
4. Verify results are displayed correctly

## Troubleshooting

### CORS Errors

If you see CORS errors in the browser console:
1. Ensure the backend CORS middleware allows your frontend domain
2. Update `backend/main.py`:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-frontend-domain.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Backend Not Responding

1. Check Render logs for errors
2. Ensure the start command is correct
3. Verify requirements.txt has all dependencies

### Build Fails with "maturin failed" or Rust Errors

**Error**: `error: failed to create directory` or `maturin failed` during build  
**Cause**: Python 3.13 incompatibility with pydantic-core

**Solution**:
1. Ensure `runtime.txt` exists in project root with content: `python-3.11.8`
2. If missing, create it and push to GitHub
3. Trigger a manual redeploy on Render
4. Check that `pydantic==2.4.2` is in `backend/requirements.txt` (not 2.5.0 or higher)

### Frontend Can't Connect to Backend

1. Check the API_URL in `frontend/app.js`
2. Ensure backend is deployed and running
3. Check browser console for errors

## Monitoring

**Render.com:**
- View logs in the Render dashboard
- Monitor uptime and performance

**GitHub Pages:**
- Check deployment status in repository settings

## Cost

All services used in this guide offer free tiers:
- **Render.com**: Free tier with 750 hours/month
- **GitHub Pages**: Unlimited for public repositories
- **Netlify**: 100GB bandwidth/month free
- **Deta Space**: Completely free
- **Railway**: $5 free credit/month

## Updates

To update your deployment:

1. Make changes locally
2. Commit and push to GitHub:
```bash
git add .
git commit -m "Your update message"
git push
```
3. Render and GitHub Pages will auto-deploy
4. For Netlify, it will auto-deploy on push

## Custom Domain (Optional)

### GitHub Pages:
1. Go to Settings → Pages
2. Add your custom domain
3. Configure DNS with your domain provider

### Render:
1. Go to your service → Settings
2. Add custom domain
3. Configure DNS

### Netlify:
1. Go to Domain settings
2. Add custom domain
3. Follow DNS configuration instructions

## Support

For issues:
1. Check the logs in your hosting dashboard
2. Review the troubleshooting section
3. Open an issue on GitHub
