"""
Unit Tests for Time Management Calculator
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

import pytest
from datetime import datetime
from parser import LogParser, LogEntry
from calculator import TimeCalculator


# Sample test data
SAMPLE_LOGS = """104138	Lingesh Balamurugan	10-12-2025	10-12-2025 10:14:29	LD CHN-1 (ASC) IN - 1	Entry Granted
104138	Lingesh Balamurugan	10-12-2025	10-12-2025 12:51:32	LD CHN-1 (ASC) Cafeteria IN-1	Exit Granted
104138	Lingesh Balamurugan	10-12-2025	10-12-2025 12:51:48	LD CHN-1 (ASC) Cafeteria OUT-1	Entry Granted
104138	Lingesh Balamurugan	10-12-2025	10-12-2025 12:52:13	LD CHN-1 (ASC) Cafeteria IN-2	Exit Granted
104138	Lingesh Balamurugan	10-12-2025	10-12-2025 12:54:45	LD CHN-1 (ASC) Cafeteria OUT-1	Entry Granted
104138	Lingesh Balamurugan	10-12-2025	10-12-2025 13:16:30	LD CHN-1 (ASC) Cafeteria IN-2	Exit Granted
104138	Lingesh Balamurugan	10-12-2025	10-12-2025 13:32:26	LD CHN-1 (ASC) Cafeteria OUT-2	Entry Granted"""


class TestLogParser:
    """Test cases for LogParser"""
    
    def test_parse_logs_basic(self):
        """Test basic log parsing"""
        entries = LogParser.parse_logs(SAMPLE_LOGS)
        assert len(entries) == 7
        assert all(isinstance(e, LogEntry) for e in entries)
    
    def test_parse_logs_employee_info(self):
        """Test employee information extraction"""
        entries = LogParser.parse_logs(SAMPLE_LOGS)
        assert entries[0].employee_id == "104138"
        assert entries[0].name == "Lingesh Balamurugan"
        assert entries[0].date == "10-12-2025"
    
    def test_parse_timestamp_formats(self):
        """Test various timestamp formats"""
        entry = LogEntry(
            "123", "Test User", "10-12-2025",
            "10-12-2025 10:14:29", "IN", "Granted"
        )
        assert isinstance(entry.timestamp, datetime)
        assert entry.timestamp.hour == 10
        assert entry.timestamp.minute == 14
    
    def test_detect_cafeteria_events(self):
        """Test cafeteria event detection"""
        entries = LogParser.parse_logs(SAMPLE_LOGS)
        cafeteria_entries = [e for e in entries if e.is_cafeteria]
        assert len(cafeteria_entries) == 6  # All cafeteria events
    
    def test_detect_in_out_events(self):
        """Test IN/OUT event detection"""
        entries = LogParser.parse_logs(SAMPLE_LOGS)
        
        # First entry should be office IN
        assert entries[0].is_in
        assert not entries[0].is_cafeteria
        
        # Cafeteria IN should be detected
        cafeteria_in = [e for e in entries if e.is_cafeteria and e.is_in]
        assert len(cafeteria_in) == 3
    
    def test_group_by_employee_date(self):
        """Test grouping by employee and date"""
        entries = LogParser.parse_logs(SAMPLE_LOGS)
        grouped = LogParser.group_by_employee_date(entries)
        
        assert len(grouped) == 1  # One employee, one date
        key = ("104138", "10-12-2025")
        assert key in grouped
        assert len(grouped[key]) == 7
    
    def test_empty_logs(self):
        """Test handling of empty logs"""
        entries = LogParser.parse_logs("")
        assert len(entries) == 0
    
    def test_malformed_logs(self):
        """Test handling of malformed logs"""
        malformed = "invalid line\n" + SAMPLE_LOGS
        entries = LogParser.parse_logs(malformed)
        # Should skip malformed line and parse the rest
        assert len(entries) == 7


class TestTimeCalculator:
    """Test cases for TimeCalculator"""
    
    def test_calculate_basic(self):
        """Test basic calculation"""
        entries = LogParser.parse_logs(SAMPLE_LOGS)
        result = TimeCalculator.calculate_logout_time(entries)
        
        assert result["employee_id"] == "104138"
        assert result["name"] == "Lingesh Balamurugan"
        assert result["date"] == "10-12-2025"
    
    def test_first_in_detection(self):
        """Test first office IN detection"""
        entries = LogParser.parse_logs(SAMPLE_LOGS)
        result = TimeCalculator.calculate_logout_time(entries)
        
        assert result["first_in"] is not None
        assert "10:14:29" in result["first_in"]
    
    def test_cafeteria_time_calculation(self):
        """Test cafeteria time calculation"""
        entries = LogParser.parse_logs(SAMPLE_LOGS)
        result = TimeCalculator.calculate_logout_time(entries)
        
        # Should have some cafeteria time
        assert result["total_cafeteria_seconds"] > 0
        assert result["total_cafeteria_duration"] != "0s"
    
    def test_net_office_time(self):
        """Test net office time calculation"""
        entries = LogParser.parse_logs(SAMPLE_LOGS)
        result = TimeCalculator.calculate_logout_time(entries)
        
        # Net time should be less than total time due to cafeteria breaks
        assert result["net_in_office_seconds"] > 0
    
    def test_expected_logout(self):
        """Test expected logout calculation"""
        entries = LogParser.parse_logs(SAMPLE_LOGS)
        result = TimeCalculator.calculate_logout_time(entries)
        
        # Should have expected logout or be completed
        assert result["expected_logout"] is not None or result["status"] == "completed"
    
    def test_8_hour_requirement(self):
        """Test 8-hour requirement calculation"""
        entries = LogParser.parse_logs(SAMPLE_LOGS)
        result = TimeCalculator.calculate_logout_time(entries)
        
        # Should calculate remaining time for 8 hours
        assert "required_seconds_for_8_hours" in result
        assert result["required_seconds_for_8_hours"] >= 0
    
    def test_duration_formatting(self):
        """Test duration formatting"""
        assert TimeCalculator._format_duration(3661) == "1h 1m 1s"
        assert TimeCalculator._format_duration(61) == "1m 1s"
        assert TimeCalculator._format_duration(30) == "30s"
        assert TimeCalculator._format_duration(7200) == "2h 0m 0s"
    
    def test_no_entries_error(self):
        """Test error handling for no entries"""
        with pytest.raises(ValueError):
            TimeCalculator.calculate_logout_time([])
    
    def test_multiple_cafeteria_sessions(self):
        """Test handling of multiple cafeteria sessions"""
        entries = LogParser.parse_logs(SAMPLE_LOGS)
        cafeteria_time = TimeCalculator._calculate_cafeteria_time(entries)
        
        # Should sum all cafeteria sessions
        assert cafeteria_time > 0


class TestIntegration:
    """Integration tests"""
    
    def test_full_workflow(self):
        """Test complete workflow from parsing to calculation"""
        # Parse logs
        entries = LogParser.parse_logs(SAMPLE_LOGS)
        assert len(entries) > 0
        
        # Group by employee/date
        grouped = LogParser.group_by_employee_date(entries)
        assert len(grouped) > 0
        
        # Calculate for first group
        first_key = list(grouped.keys())[0]
        result = TimeCalculator.calculate_logout_time(grouped[first_key])
        
        # Verify all required fields
        required_fields = [
            "employee_id", "name", "date", "first_in",
            "total_cafeteria_seconds", "net_in_office_seconds",
            "required_seconds_for_8_hours", "status"
        ]
        for field in required_fields:
            assert field in result
    
    def test_different_date_formats(self):
        """Test handling of different date formats"""
        logs_with_different_format = """104138	Test User	2025-12-10	2025-12-10 10:14:29	IN - 1	Entry Granted"""
        entries = LogParser.parse_logs(logs_with_different_format)
        assert len(entries) == 1
        assert isinstance(entries[0].timestamp, datetime)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
