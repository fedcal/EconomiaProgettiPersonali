"""
Engagement Analyzer - Analizza l'engagement degli utenti
"""

import pandas as pd
from typing import Dict, Any
from .base_analyzer import BaseAnalyzer


class EngagementAnalyzer(BaseAnalyzer):
    """Analizzatore dell'engagement"""
    
    def __init__(self):
        super().__init__('EngagementAnalyzer')
    
    def analyze(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Analizza l'engagement"""
        self.results = {
            'avg_time_on_page': self._avg_time_on_page(data),
            'avg_time_on_site': self._avg_time_on_site(data),
            'pages_per_session': self._pages_per_session(data),
            'scroll_depth': self._scroll_depth(data),
            'click_through_rate': self._click_through_rate(data),
            'video_engagement': self._video_engagement(data),
            'social_interactions': self._social_interactions(data),
            'form_interactions': self._form_interactions(data)
        }
        return self.results
    
    def _avg_time_on_page(self, data: pd.DataFrame) -> float:
        """Tempo medio sulla pagina"""
        if 'time_on_page' in data.columns:
            return float(data['time_on_page'].mean())
        return 0.0
    
    def _avg_time_on_site(self, data: pd.DataFrame) -> float:
        """Tempo medio sul sito"""
        if 'session_duration' in data.columns:
            return float(data['session_duration'].mean())
        return 0.0
    
    def _pages_per_session(self, data: pd.DataFrame) -> float:
        """Pagine per sessione"""
        if 'pageviews' in data.columns and 'sessions' in data.columns:
            total_pages = data['pageviews'].sum()
            total_sessions = data['sessions'].sum()
            return total_pages / total_sessions if total_sessions > 0 else 0
        return 0.0
    
    def _scroll_depth(self, data: pd.DataFrame) -> Dict[str, float]:
        """Profondità di scroll"""
        scroll_data = {}
        
        if 'scroll_depth' in data.columns:
            scroll_data['avg_scroll_depth'] = float(data['scroll_depth'].mean())
            scroll_data['max_scroll_depth'] = float(data['scroll_depth'].max())
        
        return scroll_data
    
    def _click_through_rate(self, data: pd.DataFrame) -> Dict[str, float]:
        """Click through rate"""
        ctr_data = {}
        
        if 'clicks' in data.columns and 'impressions' in data.columns:
            total_clicks = data['clicks'].sum()
            total_impressions = data['impressions'].sum()
            ctr_data['ctr'] = (total_clicks / total_impressions * 100) if total_impressions > 0 else 0
        
        return ctr_data
    
    def _video_engagement(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Engagement video"""
        video_data = {}
        
        if 'video_plays' in data.columns:
            video_data['total_plays'] = int(data['video_plays'].sum())
            video_data['avg_watch_time'] = float(data['watch_time'].mean()) if 'watch_time' in data.columns else 0
            video_data['completion_rate'] = float(data['video_completed'].sum() / data['video_plays'].sum() * 100) if 'video_completed' in data.columns else 0
        
        return video_data
    
    def _social_interactions(self, data: pd.DataFrame) -> Dict[str, int]:
        """Interazioni social"""
        social_data = {}
        
        social_cols = [col for col in data.columns if 'social' in col.lower() or col in ['shares', 'likes', 'comments']]
        for col in social_cols:
            social_data[col] = int(data[col].sum()) if col in data.columns else 0
        
        return social_data
    
    def _form_interactions(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Interazioni con form"""
        form_data = {}
        
        if 'form_starts' in data.columns:
            form_data['form_starts'] = int(data['form_starts'].sum())
            form_data['form_completions'] = int(data['form_completions'].sum()) if 'form_completions' in data.columns else 0
            if form_data['form_starts'] > 0:
                form_data['form_completion_rate'] = form_data['form_completions'] / form_data['form_starts'] * 100
        
        return form_data
