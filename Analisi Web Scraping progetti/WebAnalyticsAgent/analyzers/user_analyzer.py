"""
User Analyzer - Analizza il comportamento degli utenti
"""

import pandas as pd
from typing import Dict, Any
from .base_analyzer import BaseAnalyzer


class UserAnalyzer(BaseAnalyzer):
    """Analizzatore del comportamento utenti"""
    
    def __init__(self):
        super().__init__('UserAnalyzer')
    
    def analyze(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Analizza gli utenti"""
        self.results = {
            'total_users': self._count_total_users(data),
            'new_users': self._count_new_users(data),
            'returning_users': self._count_returning_users(data),
            'user_segments': self._segment_users(data),
            'user_retention': self._calculate_retention(data),
            'user_lifetime_value': self._calculate_ltv(data),
            'avg_users_per_session': self._avg_users_per_session(data)
        }
        return self.results
    
    def _count_total_users(self, data: pd.DataFrame) -> int:
        """Conta gli utenti totali"""
        if 'user_id' in data.columns:
            return data['user_id'].nunique()
        return data.shape[0]
    
    def _count_new_users(self, data: pd.DataFrame) -> int:
        """Conta nuovi utenti"""
        if 'user_type' in data.columns:
            return (data['user_type'] == 'new').sum()
        return 0
    
    def _count_returning_users(self, data: pd.DataFrame) -> int:
        """Conta utenti di ritorno"""
        if 'user_type' in data.columns:
            return (data['user_type'] == 'returning').sum()
        return 0
    
    def _segment_users(self, data: pd.DataFrame) -> Dict[str, int]:
        """Segmenta gli utenti"""
        segments = {}
        
        if 'user_segment' in data.columns:
            segments = data['user_segment'].value_counts().to_dict()
        elif 'region' in data.columns or 'country' in data.columns:
            col = 'region' if 'region' in data.columns else 'country'
            segments = data[col].value_counts().head(10).to_dict()
        
        return segments
    
    def _calculate_retention(self, data: pd.DataFrame) -> float:
        """Calcola retention rate"""
        if 'user_type' in data.columns:
            total = len(data)
            returning = (data['user_type'] == 'returning').sum()
            return (returning / total * 100) if total > 0 else 0
        return 0.0
    
    def _calculate_ltv(self, data: pd.DataFrame) -> Dict[str, float]:
        """Calcola Lifetime Value"""
        ltv_data = {}
        
        if 'revenue' in data.columns and 'user_id' in data.columns:
            ltv_data['total_revenue'] = float(data['revenue'].sum())
            ltv_data['avg_revenue_per_user'] = float(data.groupby('user_id')['revenue'].sum().mean())
        
        return ltv_data
    
    def _avg_users_per_session(self, data: pd.DataFrame) -> float:
        """Calcola media utenti per sessione"""
        if 'session_id' in data.columns and 'user_id' in data.columns:
            users_per_session = data.groupby('session_id')['user_id'].nunique()
            return float(users_per_session.mean())
        return 0.0
