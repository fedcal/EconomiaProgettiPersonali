"""
Traffic Analyzer - Analizza il traffico web
"""

import pandas as pd
from typing import Dict, Any
from .base_analyzer import BaseAnalyzer


class TrafficAnalyzer(BaseAnalyzer):
    """Analizzatore del traffico web"""
    
    def __init__(self):
        super().__init__('TrafficAnalyzer')
    
    def analyze(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Analizza il traffico web"""
        self.results = {
            'total_sessions': len(data) if len(data) > 0 else 0,
            'total_pageviews': self._count_pageviews(data),
            'unique_visitors': self._count_unique_visitors(data),
            'bounce_rate': self._calculate_bounce_rate(data),
            'avg_session_duration': self._calculate_avg_duration(data),
            'pages_per_session': self._calculate_pages_per_session(data),
            'top_pages': self._get_top_pages(data),
            'traffic_sources': self._get_traffic_sources(data),
            'hourly_distribution': self._hourly_distribution(data),
            'daily_trend': self._daily_trend(data)
        }
        return self.results
    
    def _count_pageviews(self, data: pd.DataFrame) -> int:
        """Conta le pageviews"""
        if 'pageviews' in data.columns:
            return int(data['pageviews'].sum())
        return len(data)
    
    def _count_unique_visitors(self, data: pd.DataFrame) -> int:
        """Conta i visitatori unici"""
        if 'user_id' in data.columns:
            return data['user_id'].nunique()
        return data.shape[0]
    
    def _calculate_bounce_rate(self, data: pd.DataFrame) -> float:
        """Calcola bounce rate"""
        if 'bounced' in data.columns:
            bounces = (data['bounced'] == 1).sum()
            return (bounces / len(data) * 100) if len(data) > 0 else 0
        return 0.0
    
    def _calculate_avg_duration(self, data: pd.DataFrame) -> float:
        """Calcola durata media sessione"""
        if 'session_duration' in data.columns:
            return float(data['session_duration'].mean())
        return 0.0
    
    def _calculate_pages_per_session(self, data: pd.DataFrame) -> float:
        """Calcola pagine per sessione"""
        if 'pageviews' in data.columns and 'sessions' in data.columns:
            total_pages = data['pageviews'].sum()
            total_sessions = data['sessions'].sum()
            return total_pages / total_sessions if total_sessions > 0 else 0
        return 0.0
    
    def _get_top_pages(self, data: pd.DataFrame, limit: int = 10) -> list:
        """Ritorna top pagine"""
        if 'page' in data.columns or 'page_path' in data.columns:
            col = 'page' if 'page' in data.columns else 'page_path'
            return data[col].value_counts().head(limit).to_dict()
        return {}
    
    def _get_traffic_sources(self, data: pd.DataFrame) -> Dict[str, int]:
        """Ritorna sorgenti di traffico"""
        if 'source' in data.columns or 'traffic_source' in data.columns:
            col = 'source' if 'source' in data.columns else 'traffic_source'
            return data[col].value_counts().to_dict()
        return {}
    
    def _hourly_distribution(self, data: pd.DataFrame) -> Dict[str, int]:
        """Distribuzione oraria del traffico"""
        if 'hour' in data.columns or 'timestamp' in data.columns:
            if 'hour' not in data.columns:
                data['hour'] = pd.to_datetime(data['timestamp']).dt.hour
            return data['hour'].value_counts().sort_index().to_dict()
        return {}
    
    def _daily_trend(self, data: pd.DataFrame) -> Dict[str, int]:
        """Trend giornaliero"""
        if 'date' in data.columns or 'timestamp' in data.columns:
            if 'date' not in data.columns:
                data['date'] = pd.to_datetime(data['timestamp']).dt.date
            return data['date'].value_counts().sort_index().to_dict()
        return {}
