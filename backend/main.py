"""
FastAPI Backend for Time Management Calculator
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import uvicorn

from parser import LogParser
from calculator import TimeCalculator


app = FastAPI(
    title="Time Management Calculator API",
    description="Calculate logout time based on time-management logs",
    version="1.0.0"
)

# Enable CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class LogRequest(BaseModel):
    """Request model for log calculation"""
    logs: str


class CalculationResponse(BaseModel):
    """Response model for calculation results"""
    employee_id: str
    name: str
    date: str
    first_in: Optional[str]
    last_out: Optional[str]
    total_cafeteria_seconds: int
    total_cafeteria_duration: str
    net_in_office_seconds: int
    net_in_office_duration: str
    required_seconds_for_8_hours: int
    remaining_duration: str
    expected_logout: Optional[str]
    status: str


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Time Management Calculator API",
        "version": "1.0.0",
        "endpoints": {
            "POST /calculate": "Calculate logout time from logs",
            "GET /health": "Health check"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


@app.post("/calculate", response_model=CalculationResponse)
async def calculate_logout(request: LogRequest):
    """
    Calculate logout time from time-management logs
    
    Args:
        request: LogRequest containing raw log entries
        
    Returns:
        CalculationResponse with calculated results
        
    Raises:
        HTTPException: If parsing or calculation fails
    """
    try:
        # Parse the logs
        entries = LogParser.parse_logs(request.logs)
        
        if not entries:
            raise HTTPException(
                status_code=400,
                detail="No valid log entries found. Please check your input format."
            )
        
        # Group by employee and date
        grouped = LogParser.group_by_employee_date(entries)
        
        # For now, process the first group (can be extended for multiple employees/dates)
        if not grouped:
            raise HTTPException(
                status_code=400,
                detail="Unable to group log entries."
            )
        
        # Get the first group
        first_key = list(grouped.keys())[0]
        employee_entries = grouped[first_key]
        
        # Calculate logout time
        result = TimeCalculator.calculate_logout_time(employee_entries)
        
        return result
        
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=f"Validation error: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )


if __name__ == "__main__":
    # Run the server
    uvicorn.run(app, host="0.0.0.0", port=8000)
