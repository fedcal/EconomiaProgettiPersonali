"""
Geographic Analyzer - Analizza dati geografici
"""

import pandas as pd
from typing import Dict, Any
from .base_analyzer import BaseAnalyzer


class GeographicAnalyzer(BaseAnalyzer):
    """Analizzatore dati geografici"""
    
    def __init__(self):
        super().__init__('GeographicAnalyzer')
    
    def analyze(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Analizza dati geografici"""
        self.results = {
            'countries': self._analyze_countries(data),
            'regions': self._analyze_regions(data),
            'cities': self._analyze_cities(data),
            'geographic_performance': self._geographic_performance(data)
        }
        return self.results
    
    def _analyze_countries(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Analizza dati per paese"""
        countries = {}
        
        if 'country' in data.columns:
            country_stats = data['country'].value_counts().head(10)
            for country, count in country_stats.items():
                countries[str(country)] = {
                    'sessions': int(count),
                    'percentage': float(count / len(data) * 100)
                }
        
        return countries
    
    def _analyze_regions(self, data: pd.DataFrame) -> Dict[str, int]:
        """Analizza dati per regione"""
        regions = {}
        
        if 'region' in data.columns:
            regions = data['region'].value_counts().head(10).to_dict()
        elif 'state' in data.columns:
            regions = data['state'].value_counts().head(10).to_dict()
        
        return regions
    
    def _analyze_cities(self, data: pd.DataFrame) -> Dict[str, int]:
        """Analizza dati per città"""
        cities = {}
        
        if 'city' in data.columns:
            cities = data['city'].value_counts().head(10).to_dict()
        
        return cities
    
    def _geographic_performance(self, data: pd.DataFrame) -> Dict[str, Dict]:
        """Performance per area geografica"""
        performance = {}
        
        if 'country' in data.columns:
            for country in data['country'].unique():
                country_data = data[data['country'] == country]
                
                perf = {
                    'sessions': len(country_data),
                    'avg_session_duration': float(country_data['session_duration'].mean()) if 'session_duration' in country_data.columns else 0,
                    'bounce_rate': float((country_data['bounced'] == 1).sum() / len(country_data) * 100) if 'bounced' in country_data.columns else 0,
                    'conversion_rate': float((country_data['converted'] == 1).sum() / len(country_data) * 100) if 'converted' in country_data.columns else 0
                }
                
                performance[str(country)] = perf
        
        return performance
