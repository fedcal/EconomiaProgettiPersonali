"""
Base Analyzer - Classe base per tutti gli analizzatori
"""

import pandas as pd
from typing import Dict, Any, List
import logging

logger = logging.getLogger(__name__)


class BaseAnalyzer:
    """Classe base per gli analizzatori"""
    
    def __init__(self, name: str):
        """
        Inizializza l'analizzatore
        
        Args:
            name: Nome dell'analizzatore
        """
        self.name = name
        self.results = {}
    
    def analyze(self, data: pd.DataFrame) -> Dict[str, Any]:
        """
        Analizza i dati
        
        Args:
            data: DataFrame con i dati
        
        Returns:
            Dizionario con risultati analisi
        """
        raise NotImplementedError("analyze() deve essere implementato")
    
    def _validate_columns(self, data: pd.DataFrame, required_cols: List[str]) -> bool:
        """Valida la presenza di colonne richieste"""
        missing = [col for col in required_cols if col not in data.columns]
        if missing:
            logger.warning(f"⚠️  {self.name}: Colonne mancanti: {missing}")
            return False
        return True
    
    def _clean_numeric(self, value):
        """Pulisce valori numerici"""
        try:
            return float(value) if value else 0
        except (ValueError, TypeError):
            return 0
    
    def get_results(self) -> Dict[str, Any]:
        """Ritorna i risultati dell'analisi"""
        return self.results
