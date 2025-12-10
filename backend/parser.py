"""
Time Management Log Parser
Parses raw time-management entries and extracts structured data
"""

from datetime import datetime
from typing import List, Dict, Optional
import re


class LogEntry:
    """Represents a single time-management log entry"""
    
    def __init__(self, employee_id: str, name: str, date: str, 
                 timestamp: str, event_type: str, status: str):
        self.employee_id = employee_id
        self.name = name
        self.date = date
        self.timestamp = self.parse_timestamp(timestamp)
        self.event_type = event_type
        self.status = status
        self.is_cafeteria = self.detect_cafeteria()
        self.is_in = self.detect_in_event()
        self.is_out = self.detect_out_event()
    
    def parse_timestamp(self, timestamp_str: str) -> datetime:
        """Parse timestamp from various formats"""
        # Support formats: dd-mm-yyyy HH:MM:SS, yyyy-mm-dd HH:MM:SS
        formats = [
            "%d-%m-%Y %H:%M:%S",
            "%Y-%m-%d %H:%M:%S",
            "%d/%m/%Y %H:%M:%S",
            "%Y/%m/%d %H:%M:%S",
        ]
        
        for fmt in formats:
            try:
                return datetime.strptime(timestamp_str.strip(), fmt)
            except ValueError:
                continue
        
        raise ValueError(f"Unable to parse timestamp: {timestamp_str}")
    
    def detect_cafeteria(self) -> bool:
        """Detect if this is a cafeteria event"""
        return "cafeteria" in self.event_type.lower()
    
    def detect_in_event(self) -> bool:
        """Detect if this is an IN event"""
        event_lower = self.event_type.lower()
        # Cafeteria IN means leaving office (exit)
        if self.is_cafeteria:
            return "in" in event_lower
        # Regular IN means entering office
        return "in" in event_lower and "out" not in event_lower
    
    def detect_out_event(self) -> bool:
        """Detect if this is an OUT event"""
        event_lower = self.event_type.lower()
        # Cafeteria OUT means returning to office (entry)
        if self.is_cafeteria:
            return "out" in event_lower
        # Regular OUT means leaving office
        return "out" in event_lower


class LogParser:
    """Parses raw time-management logs"""
    
    @staticmethod
    def parse_logs(raw_logs: str) -> List[LogEntry]:
        """
        Parse raw log entries into structured LogEntry objects
        
        Args:
            raw_logs: Raw text containing tab/space-separated log entries
            
        Returns:
            List of LogEntry objects
        """
        entries = []
        lines = raw_logs.strip().split('\n')
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            try:
                # Split by tab or multiple spaces
                parts = re.split(r'\t+|\s{2,}', line)
                
                # Handle different field counts (some logs may have extra fields)
                if len(parts) >= 6:
                    employee_id = parts[0].strip()
                    name = parts[1].strip()
                    date = parts[2].strip()
                    timestamp = parts[3].strip()
                    event_type = parts[4].strip()
                    status = parts[5].strip() if len(parts) > 5 else ""
                    
                    entry = LogEntry(employee_id, name, date, timestamp, 
                                   event_type, status)
                    entries.append(entry)
                    
            except Exception as e:
                # Skip malformed lines but continue parsing
                print(f"Warning: Skipping malformed line: {line[:50]}... Error: {e}")
                continue
        
        return entries
    
    @staticmethod
    def group_by_employee_date(entries: List[LogEntry]) -> Dict[tuple, List[LogEntry]]:
        """
        Group log entries by (employee_id, date)
        
        Args:
            entries: List of LogEntry objects
            
        Returns:
            Dictionary with (employee_id, date) as key and list of entries as value
        """
        grouped = {}
        
        for entry in entries:
            key = (entry.employee_id, entry.date)
            if key not in grouped:
                grouped[key] = []
            grouped[key].append(entry)
        
        # Sort entries by timestamp within each group
        for key in grouped:
            grouped[key].sort(key=lambda x: x.timestamp)
        
        return grouped
