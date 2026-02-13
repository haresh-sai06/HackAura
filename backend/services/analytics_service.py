from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import logging
from app.models.analytics import CallAnalytics
from config import settings

logger = logging.getLogger(__name__)


class AnalyticsService:
    def __init__(self):
        self.analytics = CallAnalytics()
        self.call_details = []  # Store detailed call information
        
    def record_call(
        self,
        call_sid: str,
        duration: int,
        is_emergency: bool = False,
        call_type: str = "standard",
        outcome: str = "completed",
        response_time: Optional[int] = None,
        team_member_id: Optional[str] = None,
        caller_location: Optional[str] = None,
        quality_score: Optional[float] = None
    ):
        """Record a call with detailed analytics"""
        # Record in main analytics
        self.analytics.record_call(
            call_sid=call_sid,
            duration=duration,
            is_emergency=is_emergency,
            call_type=call_type,
            outcome=outcome,
            response_time=response_time,
            team_member_id=team_member_id
        )
        
        # Store detailed call information
        call_detail = {
            "call_sid": call_sid,
            "duration": duration,
            "is_emergency": is_emergency,
            "call_type": call_type,
            "outcome": outcome,
            "response_time": response_time,
            "team_member_id": team_member_id,
            "caller_location": caller_location,
            "quality_score": quality_score,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        self.call_details.append(call_detail)
        logger.info(f"Recorded call analytics: {call_sid}")
        
    def get_dashboard_data(self) -> Dict[str, Any]:
        """Get comprehensive dashboard data"""
        summary = self.analytics.get_summary()
        daily_stats = self.analytics.get_daily_stats(7)  # Last 7 days
        
        # Calculate additional metrics
        recent_calls = self.get_recent_calls(limit=100)
        
        # Call volume trend
        call_volume_trend = self._calculate_call_volume_trend()
        
        # Response time trends
        response_time_trend = self._calculate_response_time_trend()
        
        # Team performance
        team_performance = self._get_team_performance_metrics()
        
        # Quality metrics
        quality_metrics = self._calculate_quality_metrics()
        
        return {
            "summary": summary,
            "daily_stats": daily_stats,
            "call_volume_trend": call_volume_trend,
            "response_time_trend": response_time_trend,
            "team_performance": team_performance,
            "quality_metrics": quality_metrics,
            "recent_calls": recent_calls[:10]  # Last 10 calls
        }
        
    def _calculate_call_volume_trend(self) -> Dict[str, Any]:
        """Calculate call volume trends"""
        now = datetime.utcnow()
        periods = {
            "last_hour": now - timedelta(hours=1),
            "last_24h": now - timedelta(hours=24),
            "last_7d": now - timedelta(days=7),
            "last_30d": now - timedelta(days=30)
        }
        
        trends = {}
        for period_name, start_time in periods.items():
            calls_in_period = [
                call for call in self.call_details
                if datetime.fromisoformat(call["timestamp"]) >= start_time
            ]
            trends[period_name] = len(calls_in_period)
            
        return trends
        
    def _calculate_response_time_trend(self) -> Dict[str, Any]:
        """Calculate response time trends"""
        recent_calls = [
            call for call in self.call_details
            if call["response_time"] is not None and
            datetime.fromisoformat(call["timestamp"]) >= datetime.utcnow() - timedelta(days=7)
        ]
        
        if not recent_calls:
            return {"average": 0, "trend": "stable"}
            
        avg_response_time = sum(call["response_time"] for call in recent_calls) / len(recent_calls)
        
        # Calculate trend (simple comparison with previous period)
        mid_point = len(recent_calls) // 2
        first_half = recent_calls[:mid_point]
        second_half = recent_calls[mid_point:]
        
        if first_half and second_half:
            first_avg = sum(call["response_time"] for call in first_half) / len(first_half)
            second_avg = sum(call["response_time"] for call in second_half) / len(second_half)
            
            if second_avg > first_avg * 1.1:
                trend = "increasing"
            elif second_avg < first_avg * 0.9:
                trend = "decreasing"
            else:
                trend = "stable"
        else:
            trend = "stable"
            
        return {
            "average": avg_response_time,
            "trend": trend,
            "sample_size": len(recent_calls)
        }
        
    def _get_team_performance_metrics(self) -> Dict[str, Any]:
        """Get team performance metrics"""
        team_stats = self.analytics.team_performance
        
        # Calculate additional metrics
        for member_id, stats in team_stats.items():
            # Get calls for this team member
            member_calls = [
                call for call in self.call_details
                if call["team_member_id"] == member_id
            ]
            
            # Calculate success rate
            completed_calls = len([c for c in member_calls if c["outcome"] == "completed"])
            stats["success_rate"] = (completed_calls / len(member_calls) * 100) if member_calls else 0
            
            # Calculate average call duration
            total_duration = sum(c["duration"] for c in member_calls)
            stats["avg_call_duration"] = total_duration / len(member_calls) if member_calls else 0
            
        return team_stats
        
    def _calculate_quality_metrics(self) -> Dict[str, Any]:
        """Calculate quality metrics"""
        calls_with_quality = [
            call for call in self.call_details
            if call["quality_score"] is not None
        ]
        
        if not calls_with_quality:
            return {"average_quality": 0, "total_rated_calls": 0}
            
        avg_quality = sum(call["quality_score"] for call in calls_with_quality) / len(calls_with_quality)
        
        # Quality distribution
        quality_ranges = {
            "excellent": 0,  # 4.5-5.0
            "good": 0,        # 3.5-4.5
            "average": 0,     # 2.5-3.5
            "poor": 0         # <2.5
        }
        
        for call in calls_with_quality:
            score = call["quality_score"]
            if score >= 4.5:
                quality_ranges["excellent"] += 1
            elif score >= 3.5:
                quality_ranges["good"] += 1
            elif score >= 2.5:
                quality_ranges["average"] += 1
            else:
                quality_ranges["poor"] += 1
                
        return {
            "average_quality": avg_quality,
            "total_rated_calls": len(calls_with_quality),
            "quality_distribution": quality_ranges
        }
        
    def get_recent_calls(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get recent calls"""
        recent_calls = sorted(
            self.call_details,
            key=lambda x: datetime.fromisoformat(x["timestamp"]),
            reverse=True
        )
        return recent_calls[:limit]
        
    def get_call_analytics(self, call_sid: str) -> Optional[Dict[str, Any]]:
        """Get detailed analytics for a specific call"""
        for call in self.call_details:
            if call["call_sid"] == call_sid:
                return call
        return None
        
    def get_performance_report(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> Dict[str, Any]:
        """Generate performance report for a date range"""
        if not start_date:
            start_date = datetime.utcnow() - timedelta(days=30)
        if not end_date:
            end_date = datetime.utcnow()
            
        # Filter calls by date range
        filtered_calls = [
            call for call in self.call_details
            if start_date <= datetime.fromisoformat(call["timestamp"]) <= end_date
        ]
        
        # Calculate metrics
        total_calls = len(filtered_calls)
        emergency_calls = len([c for c in filtered_calls if c["is_emergency"]])
        total_duration = sum(c["duration"] for c in filtered_calls)
        avg_duration = total_duration / total_calls if total_calls > 0 else 0
        
        # Response times
        response_times = [c["response_time"] for c in filtered_calls if c["response_time"] is not None]
        avg_response_time = sum(response_times) / len(response_times) if response_times else 0
        
        # Outcomes
        outcomes = {}
        for call in filtered_calls:
            outcome = call["outcome"]
            outcomes[outcome] = outcomes.get(outcome, 0) + 1
            
        return {
            "period": {
                "start_date": start_date.isoformat(),
                "end_date": end_date.isoformat()
            },
            "summary": {
                "total_calls": total_calls,
                "emergency_calls": emergency_calls,
                "emergency_rate": (emergency_calls / total_calls * 100) if total_calls > 0 else 0,
                "avg_duration_seconds": avg_duration,
                "avg_response_time_seconds": avg_response_time
            },
            "outcomes": outcomes,
            "detailed_calls": filtered_calls
        }
        
    def export_analytics(self, format: str = "json") -> Dict[str, Any]:
        """Export analytics data"""
        data = {
            "dashboard_data": self.get_dashboard_data(),
            "performance_report": self.get_performance_report(),
            "export_timestamp": datetime.utcnow().isoformat()
        }
        
        if format.lower() == "csv":
            # Convert to CSV-friendly format
            return self._convert_to_csv(data)
        
        return data
        
    def _convert_to_csv(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Convert analytics data to CSV format"""
        # This would implement CSV conversion logic
        # For now, return the data as-is
        return data


# Global instance
analytics_service = AnalyticsService()
