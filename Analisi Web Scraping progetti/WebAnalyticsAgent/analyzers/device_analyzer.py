"""
Device Analyzer - Analizza dati dispositivi
"""

import pandas as pd
from typing import Dict, Any
from .base_analyzer import BaseAnalyzer


class DeviceAnalyzer(BaseAnalyzer):
    """Analizzatore dispositivi"""
    
    def __init__(self):
        super().__init__('DeviceAnalyzer')
    
    def analyze(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Analizza dispositivi"""
        self.results = {
            'device_types': self._analyze_device_types(data),
            'operating_systems': self._analyze_os(data),
            'browsers': self._analyze_browsers(data),
            'screen_resolutions': self._analyze_resolutions(data),
            'device_performance': self._device_performance(data)
        }
        return self.results
    
    def _analyze_device_types(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Analizza tipi di dispositivo"""
        devices = {}
        
        if 'device_type' in data.columns or 'device' in data.columns:
            col = 'device_type' if 'device_type' in data.columns else 'device'
            device_stats = data[col].value_counts()
            for device, count in device_stats.items():
                devices[str(device)] = {
                    'sessions': int(count),
                    'percentage': float(count / len(data) * 100)
                }
        
        return devices
    
    def _analyze_os(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Analizza sistemi operativi"""
        os_data = {}
        
        if 'os' in data.columns or 'operating_system' in data.columns:
            col = 'os' if 'os' in data.columns else 'operating_system'
            os_stats = data[col].value_counts()
            for os, count in os_stats.items():
                os_data[str(os)] = {
                    'sessions': int(count),
                    'percentage': float(count / len(data) * 100)
                }
        
        return os_data
    
    def _analyze_browsers(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Analizza browser"""
        browsers = {}
        
        if 'browser' in data.columns:
            browser_stats = data['browser'].value_counts().head(10)
            for browser, count in browser_stats.items():
                browsers[str(browser)] = {
                    'sessions': int(count),
                    'percentage': float(count / len(data) * 100)
                }
        
        return browsers
    
    def _analyze_resolutions(self, data: pd.DataFrame) -> Dict[str, int]:
        """Analizza risoluzioni schermo"""
        resolutions = {}
        
        if 'screen_resolution' in data.columns:
            resolutions = data['screen_resolution'].value_counts().head(10).to_dict()
        
        return resolutions
    
    def _device_performance(self, data: pd.DataFrame) -> Dict[str, Dict]:
        """Performance per dispositivo"""
        performance = {}
        
        if 'device_type' in data.columns or 'device' in data.columns:
            col = 'device_type' if 'device_type' in data.columns else 'device'
            
            for device in data[col].unique():
                device_data = data[data[col] == device]
                
                perf = {
                    'sessions': len(device_data),
                    'avg_session_duration': float(device_data['session_duration'].mean()) if 'session_duration' in device_data.columns else 0,
                    'bounce_rate': float((device_data['bounced'] == 1).sum() / len(device_data) * 100) if 'bounced' in device_data.columns else 0,
                    'conversion_rate': float((device_data['converted'] == 1).sum() / len(device_data) * 100) if 'converted' in device_data.columns else 0
                }
                
                performance[str(device)] = perf
        
        return performance
