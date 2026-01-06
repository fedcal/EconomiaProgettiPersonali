"""
Data Exporter - Esporta i dati analizzati
"""

import json
import os
import csv
from datetime import datetime
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)


class DataExporter:
    """Esportatore dati"""
    
    def __init__(self, export_format: str = 'json'):
        """
        Inizializza l'esportatore
        
        Args:
            export_format: Formato esportazione (json, csv, etc.)
        """
        self.format = export_format
    
    def export(self, data: Dict[str, Any], output_dir: str = './exports') -> str:
        """
        Esporta i dati
        
        Args:
            data: Dati da esportare
            output_dir: Cartella output
        
        Returns:
            Percorso al file esportato
        """
        os.makedirs(output_dir, exist_ok=True)
        
        if self.format == 'json':
            return self._export_json(data, output_dir)
        elif self.format == 'csv':
            return self._export_csv(data, output_dir)
        else:
            return self._export_json(data, output_dir)
    
    def _export_json(self, data: Dict[str, Any], output_dir: str) -> str:
        """Esporta in JSON"""
        filename = f"analytics_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        filepath = os.path.join(output_dir, filename)
        
        export_data = {
            'exported_at': datetime.now().isoformat(),
            'data': data
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, default=str)
        
        logger.info(f"✅ Dati esportati in JSON: {filepath}")
        return filepath
    
    def _export_csv(self, data: Dict[str, Any], output_dir: str) -> str:
        """Esporta in CSV"""
        filename = f"analytics_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        filepath = os.path.join(output_dir, filename)
        
        # Flattena i dati per CSV
        rows = []
        for source_name, source_data in data.items():
            analysis = source_data.get('analysis', {})
            for module_name, module_data in analysis.items():
                if isinstance(module_data, dict):
                    row = {
                        'source': source_name,
                        'module': module_name,
                        'data': json.dumps(module_data)
                    }
                    rows.append(row)
        
        if rows:
            with open(filepath, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=['source', 'module', 'data'])
                writer.writeheader()
                writer.writerows(rows)
        
        logger.info(f"✅ Dati esportati in CSV: {filepath}")
        return filepath
