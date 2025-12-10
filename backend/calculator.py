"""
Time Calculator
Calculates logout time based on parsed log entries
"""

from datetime import datetime, timedelta
from typing import List, Dict, Optional
from parser import LogEntry


class TimeCalculator:
    """Calculates working hours and required logout time"""
    
    REQUIRED_HOURS = 8  # Minimum required hours in office
    
    @staticmethod
    def calculate_logout_time(entries: List[LogEntry]) -> Dict:
        """
        Calculate logout time for a set of log entries
        
        Args:
            entries: List of LogEntry objects for a single employee on a single date
            
        Returns:
            Dictionary containing calculation results
        """
        if not entries:
            raise ValueError("No entries provided")
        
        # Sort entries by timestamp
        entries.sort(key=lambda x: x.timestamp)
        
        # Get employee info
        employee_id = entries[0].employee_id
        name = entries[0].name
        date = entries[0].date
        
        # Find first office IN
        first_in = TimeCalculator._find_first_office_in(entries)
        if not first_in:
            raise ValueError("No office IN event found")
        
        # Find last office OUT (may be None if still in office)
        last_out = TimeCalculator._find_last_office_out(entries)
        
        # Calculate cafeteria time
        cafeteria_seconds = TimeCalculator._calculate_cafeteria_time(entries)
        
        # Calculate net in-office time
        if last_out:
            # If we have a last OUT, user has left - use actual time spent
            total_time = (last_out - first_in).total_seconds()
            net_in_office_seconds = total_time - cafeteria_seconds
            current_time_used = last_out
        else:
            # If no last OUT, user is still in office - use CURRENT TIME
            current_time = datetime.now()
            # Use current time to calculate how long they've been in office
            total_time = (current_time - first_in).total_seconds()
            net_in_office_seconds = total_time - cafeteria_seconds
            current_time_used = current_time
        
        # Calculate required seconds for 8 hours
        required_seconds = TimeCalculator.REQUIRED_HOURS * 3600
        remaining_seconds = max(0, required_seconds - net_in_office_seconds)
        
        # Calculate expected logout time
        if remaining_seconds > 0:
            if last_out:
                # If already left, can't calculate meaningful logout time
                expected_logout = None
            else:
                # Add remaining time to CURRENT TIME
                expected_logout = current_time_used + timedelta(seconds=remaining_seconds)
        else:
            # Already completed 8 hours
            expected_logout = last_out if last_out else current_time_used
        
        # Parse the date to ensure correct format
        parsed_date = TimeCalculator._parse_date(date)
        
        return {
            "employee_id": employee_id,
            "name": name,
            "date": parsed_date.strftime("%Y-%m-%d"),  # Return in ISO format (YYYY-MM-DD)
            "first_in": first_in.isoformat() if first_in else None,
            "last_out": last_out.isoformat() if last_out else None,
            "total_cafeteria_seconds": int(cafeteria_seconds),
            "total_cafeteria_duration": TimeCalculator._format_duration(cafeteria_seconds),
            "net_in_office_seconds": int(net_in_office_seconds),
            "net_in_office_duration": TimeCalculator._format_duration(net_in_office_seconds),
            "required_seconds_for_8_hours": int(remaining_seconds),
            "remaining_duration": TimeCalculator._format_duration(remaining_seconds),
            "expected_logout": expected_logout.isoformat() if expected_logout else None,
            "status": "completed" if remaining_seconds == 0 else "in_progress"
        }
    
    @staticmethod
    def _parse_date(date_str: str) -> datetime:
        """Parse date from various formats to datetime object"""
        formats = [
            "%d-%m-%Y",  # DD-MM-YYYY (most common in your logs)
            "%Y-%m-%d",  # YYYY-MM-DD (ISO format)
            "%d/%m/%Y",  # DD/MM/YYYY
            "%Y/%m/%d",  # YYYY/MM/DD
        ]
        
        for fmt in formats:
            try:
                return datetime.strptime(date_str.strip(), fmt)
            except ValueError:
                continue
        
        raise ValueError(f"Unable to parse date: {date_str}")
    
    @staticmethod
    def _find_first_office_in(entries: List[LogEntry]) -> Optional[datetime]:
        """Find the first office IN event (not cafeteria)"""
        for entry in entries:
            if not entry.is_cafeteria and entry.is_in:
                return entry.timestamp
        return None
    
    @staticmethod
    def _find_last_office_out(entries: List[LogEntry]) -> Optional[datetime]:
        """Find the last office OUT event (not cafeteria)"""
        last_out = None
        for entry in reversed(entries):
            if not entry.is_cafeteria and entry.is_out:
                return entry.timestamp
        return last_out
    
    @staticmethod
    def _calculate_cafeteria_time(entries: List[LogEntry]) -> float:
        """
        Calculate total cafeteria time (time spent outside office for breaks)
        
        Cafeteria IN = leaving office for break
        Cafeteria OUT = returning to office from break
        """
        cafeteria_sessions = []
        current_session_start = None
        
        for entry in entries:
            if entry.is_cafeteria:
                if entry.is_in:
                    # Started cafeteria break (left office)
                    current_session_start = entry.timestamp
                elif entry.is_out and current_session_start:
                    # Ended cafeteria break (returned to office)
                    cafeteria_sessions.append({
                        'start': current_session_start,
                        'end': entry.timestamp
                    })
                    current_session_start = None
        
        # Calculate total cafeteria time
        total_seconds = 0
        for session in cafeteria_sessions:
            duration = (session['end'] - session['start']).total_seconds()
            total_seconds += duration
        
        return total_seconds
    
    @staticmethod
    def _format_duration(seconds: float) -> str:
        """Format duration in seconds to human-readable format"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        
        if hours > 0:
            return f"{hours}h {minutes}m {secs}s"
        elif minutes > 0:
            return f"{minutes}m {secs}s"
        else:
            return f"{secs}s"
