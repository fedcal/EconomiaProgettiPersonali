"""
Behavioral Analyzer - Analizza il comportamento degli utenti
"""

import pandas as pd
from typing import Dict, Any
from .base_analyzer import BaseAnalyzer


class BehavioralAnalyzer(BaseAnalyzer):
    """Analizzatore del comportamento utenti"""
    
    def __init__(self):
        super().__init__('BehavioralAnalyzer')
    
    def analyze(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Analizza il comportamento"""
        self.results = {
            'user_flow': self._analyze_user_flow(data),
            'event_patterns': self._analyze_event_patterns(data),
            'session_types': self._session_types(data),
            'user_segments': self._segment_users_by_behavior(data),
            'anomalies': self._detect_anomalies(data)
        }
        return self.results
    
    def _analyze_user_flow(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Analizza il flusso utenti"""
        flow = {}
        
        if 'page' in data.columns and 'session_id' in data.columns:
            flow['page_transitions'] = self._get_page_transitions(data)
            flow['entry_pages'] = self._get_entry_pages(data)
            flow['exit_pages'] = self._get_exit_pages(data)
        
        return flow
    
    def _get_page_transitions(self, data: pd.DataFrame) -> Dict[str, int]:
        """Transizioni tra pagine"""
        transitions = {}
        
        if 'previous_page' in data.columns and 'page' in data.columns:
            for _, row in data.iterrows():
                transition = f"{row['previous_page']} → {row['page']}"
                transitions[transition] = transitions.get(transition, 0) + 1
        
        return dict(sorted(transitions.items(), key=lambda x: x[1], reverse=True)[:10])
    
    def _get_entry_pages(self, data: pd.DataFrame) -> Dict[str, int]:
        """Pagine di ingresso"""
        if 'is_first_page' in data.columns and 'page' in data.columns:
            entry = data[data['is_first_page'] == True]['page'].value_counts().head(10).to_dict()
            return entry
        return {}
    
    def _get_exit_pages(self, data: pd.DataFrame) -> Dict[str, int]:
        """Pagine di uscita"""
        if 'is_last_page' in data.columns and 'page' in data.columns:
            exit_pages = data[data['is_last_page'] == True]['page'].value_counts().head(10).to_dict()
            return exit_pages
        return {}
    
    def _analyze_event_patterns(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Analizza pattern di eventi"""
        patterns = {}
        
        if 'event' in data.columns:
            patterns['total_events'] = len(data)
            patterns['event_types'] = data['event'].value_counts().head(15).to_dict()
            patterns['events_per_session'] = float(len(data) / data['session_id'].nunique()) if 'session_id' in data.columns else 0
        
        return patterns
    
    def _session_types(self, data: pd.DataFrame) -> Dict[str, int]:
        """Tipologie di sessione"""
        session_types = {}
        
        if 'session_type' in data.columns:
            session_types = data['session_type'].value_counts().to_dict()
        
        return session_types
    
    def _segment_users_by_behavior(self, data: pd.DataFrame) -> Dict[str, int]:
        """Segmenta utenti per comportamento"""
        segments = {}
        
        if 'user_segment' in data.columns:
            segments = data['user_segment'].value_counts().to_dict()
        elif 'user_type' in data.columns:
            segments = data['user_type'].value_counts().to_dict()
        
        return segments
    
    def _detect_anomalies(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Rileva anomalie"""
        anomalies = {
            'unusual_session_durations': 0,
            'unusual_pageviews': 0,
            'bot_activity': 0
        }
        
        if 'session_duration' in data.columns:
            mean = data['session_duration'].mean()
            std = data['session_duration'].std()
            anomalies['unusual_session_durations'] = len(data[data['session_duration'] > mean + 3*std])
        
        if 'pageviews' in data.columns:
            mean = data['pageviews'].mean()
            std = data['pageviews'].std()
            anomalies['unusual_pageviews'] = len(data[data['pageviews'] > mean + 3*std])
        
        if 'bot' in data.columns:
            anomalies['bot_activity'] = int((data['bot'] == True).sum())
        
        return anomalies
