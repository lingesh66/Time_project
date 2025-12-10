# Quick Start Guide

Get the Time Management Calculator running in 5 minutes!

## 🚀 Quick Start (Local Development)

### Prerequisites
- Python 3.9 or higher
- Modern web browser (Chrome, Firefox, Edge, Safari)
- Internet connection (for TailwindCSS CDN)

### Step 1: Clone or Download
```bash
# If using Git
git clone https://github.com/YOUR_USERNAME/time-management-calculator.git
cd time-management-calculator

# Or download and extract the ZIP file
```

### Step 2: Install Backend Dependencies
```bash
# Navigate to project directory
cd Time_project

# Install Python packages
pip install fastapi uvicorn pydantic python-multipart
```

### Step 3: Start the Backend
```bash
# Run the FastAPI server
python backend/main.py
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

### Step 4: Open the Frontend
Open `frontend/index.html` in your web browser:

**Option A - Direct File:**
- Double-click `frontend/index.html`
- Or drag it into your browser

**Option B - Local Server (recommended):**
```bash
# In a new terminal, from the frontend directory
cd frontend
python -m http.server 8080
```
Then visit: `http://localhost:8080`

### Step 5: Test It Out!
1. Click the **lightning bolt** button to load sample data
2. Click **"Calculate Logout Time"**
3. See your results instantly!

## 📝 Using Your Own Data

### Input Format
Paste your logs in this format (tab or space-separated):
```
EmployeeID  Name  Date  DateTime  EventType  Status
```

Example:
```
104138	Lingesh Balamurugan	10-12-2025	10-12-2025 10:14:29	LD CHN-1 (ASC) IN - 1	Entry Granted
104138	Lingesh Balamurugan	10-12-2025	10-12-2025 12:51:32	LD CHN-1 (ASC) Cafeteria IN-1	Exit Granted
```

### Event Types
- **Office IN**: Entry to office (e.g., "IN - 1", "Entry Granted")
- **Office OUT**: Exit from office (e.g., "OUT - 1", "Exit Granted")
- **Cafeteria IN**: Going to cafeteria (e.g., "Cafeteria IN-1")
- **Cafeteria OUT**: Returning from cafeteria (e.g., "Cafeteria OUT-1")

## 🧪 Run Tests
```bash
# Install pytest
pip install pytest

# Run all tests
python -m pytest tests/test_parser.py -v

# Expected output: 19 passed in 0.15s
```

## 🌐 Deploy to Production

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed deployment instructions to:
- **Render.com** (Backend)
- **GitHub Pages** (Frontend)
- **Netlify** (Frontend alternative)
- **Railway** (Backend alternative)
- **Deta Space** (Backend alternative)

## ⚙️ Configuration

### Change API URL (for production)
Edit `frontend/app.js`:
```javascript
const CONFIG = {
    API_URL: 'https://your-backend-url.com'
};
```

### Change Required Hours
Edit `backend/calculator.py`:
```python
class TimeCalculator:
    REQUIRED_HOURS = 8  # Change to your requirement
```

## 🐛 Troubleshooting

### Backend won't start
- **Error**: `ModuleNotFoundError: No module named 'fastapi'`
- **Solution**: Run `pip install fastapi uvicorn`

### Frontend can't connect to backend
- **Error**: Network error or CORS error
- **Solution**: 
  1. Ensure backend is running on port 8000
  2. Check `CONFIG.API_URL` in `frontend/app.js`
  3. Open browser console (F12) to see detailed errors

### No results showing
- **Issue**: Clicked calculate but nothing happens
- **Solution**:
  1. Check browser console for errors (F12)
  2. Verify backend is running
  3. Ensure input format is correct
  4. Try the sample data first

### Tests failing
- **Error**: Import errors or test failures
- **Solution**:
  1. Ensure you're in the project root directory
  2. Install pytest: `pip install pytest`
  3. Check Python version: `python --version` (should be 3.9+)

## 📚 Next Steps

1. **Customize the UI**: Edit `frontend/styles.css` for your brand colors
2. **Add Features**: Extend the calculator with new functionality
3. **Deploy**: Follow [DEPLOYMENT.md](DEPLOYMENT.md) to go live
4. **Share**: Star the repo and share with colleagues!

## 💡 Tips

- **Keyboard Shortcut**: Press `Ctrl+V` to paste logs quickly
- **Sample Data**: Use the lightning bolt button to test without real data
- **Clear Input**: Click "Clear" to reset the form
- **Mobile Friendly**: Works great on phones and tablets too!

## 📖 Documentation

- **README.md**: Project overview and features
- **DOCUMENTATION.md**: Technical details and API docs
- **DEPLOYMENT.md**: Hosting and deployment guide

## 🆘 Need Help?

- Check the [DOCUMENTATION.md](DOCUMENTATION.md) for detailed explanations
- Open an issue on GitHub
- Review the test cases in `tests/test_parser.py` for examples

---

**Happy time tracking! ⏰**
