# Time Management Calculator

An open-source web application that calculates logout time for employees based on their time-management logs.

## Features

- 📊 Parse time-management logs automatically
- ⏰ Calculate required logout time (8-hour minimum)
- ☕ Track cafeteria breaks separately
- 🎯 Real-time calculation of remaining work hours
- 🎨 Modern, responsive UI with dark mode
- 🆓 100% free to host and open-source

## How It Works

1. Paste your time-management logs into the input field
2. Click "Calculate Logout Time"
3. Get instant results showing:
   - First office IN time
   - Last office OUT time (if available)
   - Total cafeteria break duration
   - Net in-office working time
   - Required logout time to complete 8 hours

## Input Format

The application accepts tab or space-separated log entries:

```
104138	Lingesh Balamurugan	10-12-2025	10-12-2025 10:14:29	LD CHN-1 (ASC) IN - 1	Entry Granted
104138	Lingesh Balamurugan	10-12-2025	10-12-2025 12:51:32	LD CHN-1 (ASC) Cafeteria IN-1	Exit Granted
104138	Lingesh Balamurugan	10-12-2025	10-12-2025 12:51:48	LD CHN-1 (ASC) Cafeteria OUT-1	Entry Granted
```

## Technology Stack

### Frontend
- HTML5
- TailwindCSS (via CDN)
- Vanilla JavaScript

### Backend
- Python 3.9+
- FastAPI
- Uvicorn

## Local Development

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the server:
```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

### Frontend Setup

1. Open `frontend/index.html` in your browser, or
2. Use a local server:
```bash
cd frontend
python -m http.server 8080
```

Visit `http://localhost:8080`

## Deployment

### Backend (Render.com)

1. Create a new Web Service on [Render](https://render.com)
2. Connect your GitHub repository
3. Configure:
   - **Build Command**: `pip install -r backend/requirements.txt`
   - **Start Command**: `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`
4. Deploy!

### Frontend (GitHub Pages)

1. Push your code to GitHub
2. Go to Settings → Pages
3. Select branch and `/frontend` folder
4. Your site will be live at `https://yourusername.github.io/time-management-app`

## API Documentation

### POST /calculate

Calculate logout time from time-management logs.

**Request Body:**
```json
{
  "logs": "104138\tLingesh Balamurugan\t10-12-2025\t10-12-2025 10:14:29\tLD CHN-1 (ASC) IN - 1\tEntry Granted\n..."
}
```

**Response:**
```json
{
  "employee_id": "104138",
  "name": "Lingesh Balamurugan",
  "date": "2025-12-10",
  "first_in": "2025-12-10T10:14:29",
  "last_out": "2025-12-10T13:32:26",
  "total_cafeteria_seconds": 1234,
  "net_in_office_seconds": 11234,
  "required_seconds_for_8_hours": 17566,
  "expected_logout": "2025-12-10T18:14:29"
}
```

## Testing

Run the test suite:
```bash
cd tests
python -m pytest test_parser.py -v
```

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

If you encounter any issues or have questions, please open an issue on GitHub.

## Author

Built with ❤️ for better time management
