from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from collections import defaultdict
import uuid


class CallAnalytics:
    def __init__(self):
        self.id = str(uuid.uuid4())
        self.total_calls = 0
        self.emergency_calls = 0
        self.call_duration_total = 0  # in seconds
        self.response_times = []  # in seconds
        self.call_types = defaultdict(int)
        self.call_outcomes = defaultdict(int)
        self.daily_stats = defaultdict(lambda: {"calls": 0, "emergencies": 0, "duration": 0})
        self.team_performance = defaultdict(lambda: {"calls_handled": 0, "avg_response_time": 0})
        self.created_at = datetime.utcnow()
        self.last_updated = datetime.utcnow()
        
    def record_call(
        self,
        call_sid: str,
        duration: int,
        is_emergency: bool = False,
        call_type: str = "standard",
        outcome: str = "completed",
        response_time: Optional[int] = None,
        team_member_id: Optional[str] = None
    ):
        """Record a call for analytics"""
        self.total_calls += 1
        self.call_duration_total += duration
        
        if is_emergency:
            self.emergency_calls += 1
            
        self.call_types[call_type] += 1
        self.call_outcomes[outcome] += 1
        
        if response_time:
            self.response_times.append(response_time)
            
        if team_member_id:
            self.team_performance[team_member_id]["calls_handled"] += 1
            if response_time:
                current_avg = self.team_performance[team_member_id]["avg_response_time"]
                calls_handled = self.team_performance[team_member_id]["calls_handled"]
                self.team_performance[team_member_id]["avg_response_time"] = (
                    (current_avg * (calls_handled - 1) + response_time) / calls_handled
                )
        
        # Update daily stats
        today = datetime.utcnow().date().isoformat()
        self.daily_stats[today]["calls"] += 1
        if is_emergency:
            self.daily_stats[today]["emergencies"] += 1
        self.daily_stats[today]["duration"] += duration
        
        self.last_updated = datetime.utcnow()
        
    def get_summary(self) -> Dict[str, Any]:
        """Get analytics summary"""
        avg_response_time = sum(self.response_times) / len(self.response_times) if self.response_times else 0
        avg_call_duration = self.call_duration_total / self.total_calls if self.total_calls > 0 else 0
        
        return {
            "total_calls": self.total_calls,
            "emergency_calls": self.emergency_calls,
            "emergency_rate": (self.emergency_calls / self.total_calls * 100) if self.total_calls > 0 else 0,
            "avg_call_duration": avg_call_duration,
            "avg_response_time": avg_response_time,
            "call_types": dict(self.call_types),
            "call_outcomes": dict(self.call_outcomes),
            "team_performance": dict(self.team_performance),
            "last_updated": self.last_updated.isoformat()
        }
        
    def get_daily_stats(self, days: int = 30) -> Dict[str, Any]:
        """Get daily statistics for the last N days"""
        end_date = datetime.utcnow().date()
        start_date = end_date - timedelta(days=days)
        
        daily_data = {}
        current_date = start_date
        
        while current_date <= end_date:
            date_key = current_date.isoformat()
            daily_data[date_key] = self.daily_stats.get(date_key, {"calls": 0, "emergencies": 0, "duration": 0})
            current_date += timedelta(days=1)
            
        return daily_data
        
    def get_peak_hours(self) -> Dict[str, int]:
        """Analyze call volume by hour of day"""
        # This would need more detailed timestamp data in a real implementation
        # For now, return a placeholder
        return {str(hour): 0 for hour in range(24)}
        
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        return {
            "id": self.id,
            "summary": self.get_summary(),
            "daily_stats": dict(self.daily_stats),
            "peak_hours": self.get_peak_hours(),
            "created_at": self.created_at.isoformat(),
            "last_updated": self.last_updated.isoformat()
        }
