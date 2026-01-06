"""
Conversion Analyzer - Analizza conversioni e obiettivi
"""

import pandas as pd
from typing import Dict, Any
from .base_analyzer import BaseAnalyzer


class ConversionAnalyzer(BaseAnalyzer):
    """Analizzatore delle conversioni"""
    
    def __init__(self):
        super().__init__('ConversionAnalyzer')
    
    def analyze(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Analizza le conversioni"""
        self.results = {
            'total_conversions': self._count_conversions(data),
            'conversion_rate': self._calculate_conversion_rate(data),
            'conversion_value': self._calculate_conversion_value(data),
            'avg_conversion_value': self._calculate_avg_conversion_value(data),
            'top_conversion_pages': self._top_conversion_pages(data),
            'conversion_by_source': self._conversion_by_source(data),
            'conversion_funnel': self._conversion_funnel(data),
            'abandoned_carts': self._abandoned_carts(data)
        }
        return self.results
    
    def _count_conversions(self, data: pd.DataFrame) -> int:
        """Conta le conversioni"""
        if 'converted' in data.columns:
            return (data['converted'] == 1).sum()
        elif 'goal_completed' in data.columns:
            return (data['goal_completed'] == 1).sum()
        return 0
    
    def _calculate_conversion_rate(self, data: pd.DataFrame) -> float:
        """Calcola conversion rate"""
        conversions = self._count_conversions(data)
        total = len(data)
        return (conversions / total * 100) if total > 0 else 0
    
    def _calculate_conversion_value(self, data: pd.DataFrame) -> float:
        """Calcola valore totale conversioni"""
        if 'conversion_value' in data.columns:
            return float(data[data['converted'] == 1]['conversion_value'].sum())
        elif 'revenue' in data.columns:
            return float(data['revenue'].sum())
        return 0.0
    
    def _calculate_avg_conversion_value(self, data: pd.DataFrame) -> float:
        """Calcola valore medio conversione"""
        total_value = self._calculate_conversion_value(data)
        conversions = self._count_conversions(data)
        return total_value / conversions if conversions > 0 else 0
    
    def _top_conversion_pages(self, data: pd.DataFrame, limit: int = 10) -> Dict[str, int]:
        """Pagine con più conversioni"""
        if 'page' in data.columns:
            converted = data[data['converted'] == 1]
            return converted['page'].value_counts().head(limit).to_dict()
        return {}
    
    def _conversion_by_source(self, data: pd.DataFrame) -> Dict[str, float]:
        """Conversioni per sorgente"""
        conversion_by_source = {}
        
        if 'source' in data.columns:
            sources = data['source'].unique()
            for source in sources:
                source_data = data[data['source'] == source]
                conversions = (source_data['converted'] == 1).sum()
                rate = (conversions / len(source_data) * 100) if len(source_data) > 0 else 0
                conversion_by_source[str(source)] = rate
        
        return conversion_by_source
    
    def _conversion_funnel(self, data: pd.DataFrame) -> Dict[str, int]:
        """Analizza il funnel di conversione"""
        funnel = {}
        
        if 'funnel_step' in data.columns:
            funnel = data['funnel_step'].value_counts().sort_index().to_dict()
        
        return funnel
    
    def _abandoned_carts(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Analizza carrelli abbandonati"""
        abandoned = {}
        
        if 'cart_status' in data.columns:
            abandoned_count = (data['cart_status'] == 'abandoned').sum()
            abandoned['abandoned_carts'] = abandoned_count
            abandoned['abandonment_rate'] = (abandoned_count / len(data) * 100) if len(data) > 0 else 0
        
        return abandoned
