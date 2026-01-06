"""
Web Analytics Agent - Agente Autonomo di Analisi Web Analytics
Analizza dati da Google Analytics, tracciamenti custom, log files e genera report dettagliati
"""

import os
import sys
import json
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import logging

# Configurazione logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class WebAnalyticsAgent:
    """Agente principale per l'analisi web analytics"""
    
    def __init__(self, config_file: Optional[str] = None):
        """
        Inizializza l'agente
        
        Args:
            config_file: Percorso al file di configurazione JSON (opzionale)
        """
        self.config = self._load_config(config_file)
        self.data_sources = {}
        self.analyzed_data = {}
        self.reports = {}
        self.timestamp = datetime.now()
        
        logger.info("🤖 Web Analytics Agent inizializzato")
    
    def _load_config(self, config_file: Optional[str] = None) -> Dict:
        """Carica la configurazione"""
        default_config = {
            'project_name': 'Web Analytics Analysis',
            'data_dir': './data',
            'output_dir': './reports',
            'supported_formats': ['csv', 'json', 'ga4'],
            'analysis_modules': [
                'traffic',
                'users',
                'conversions',
                'engagement',
                'geographic',
                'device',
                'behavioral'
            ],
            'report_format': ['html', 'pdf', 'markdown', 'json']
        }
        
        if config_file and os.path.exists(config_file):
            with open(config_file, 'r') as f:
                user_config = json.load(f)
                default_config.update(user_config)
        
        return default_config
    
    def add_data_source(self, name: str, source_type: str, path: str) -> bool:
        """
        Aggiunge una fonte dati
        
        Args:
            name: Nome identificativo della fonte
            source_type: Tipo (csv, json, ga4, log)
            path: Percorso al file dati
        
        Returns:
            True se aggiunto con successo
        """
        if not os.path.exists(path):
            logger.error(f"❌ Percorso non trovato: {path}")
            return False
        
        self.data_sources[name] = {
            'type': source_type,
            'path': path,
            'added_at': datetime.now().isoformat(),
            'status': 'pending'
        }
        
        logger.info(f"✅ Fonte dati aggiunta: {name} ({source_type})")
        return True
    
    def analyze_all_sources(self) -> Dict[str, Any]:
        """
        Analizza tutte le fonti dati aggiunte
        
        Returns:
            Dizionario con risultati analisi
        """
        logger.info(f"🔍 Inizio analisi di {len(self.data_sources)} fonti dati")
        
        from analyzers.traffic_analyzer import TrafficAnalyzer
        from analyzers.user_analyzer import UserAnalyzer
        from analyzers.conversion_analyzer import ConversionAnalyzer
        from analyzers.engagement_analyzer import EngagementAnalyzer
        from analyzers.geographic_analyzer import GeographicAnalyzer
        from analyzers.device_analyzer import DeviceAnalyzer
        from analyzers.behavioral_analyzer import BehavioralAnalyzer
        
        analyzers = {
            'traffic': TrafficAnalyzer(),
            'users': UserAnalyzer(),
            'conversions': ConversionAnalyzer(),
            'engagement': EngagementAnalyzer(),
            'geographic': GeographicAnalyzer(),
            'device': DeviceAnalyzer(),
            'behavioral': BehavioralAnalyzer()
        }
        
        for source_name, source_info in self.data_sources.items():
            logger.info(f"\n📊 Analizzando: {source_name}")
            
            try:
                # Carica i dati
                data = self._load_data(source_info)
                
                # Esegui analisi
                analysis_results = {}
                for analyzer_name, analyzer in analyzers.items():
                    if analyzer_name in self.config['analysis_modules']:
                        analysis_results[analyzer_name] = analyzer.analyze(data)
                        logger.info(f"  ✓ {analyzer_name} completato")
                
                self.analyzed_data[source_name] = {
                    'raw_data': data,
                    'analysis': analysis_results,
                    'timestamp': datetime.now().isoformat()
                }
                
                self.data_sources[source_name]['status'] = 'completed'
                
            except Exception as e:
                logger.error(f"  ❌ Errore analizzando {source_name}: {e}")
                self.data_sources[source_name]['status'] = 'failed'
        
        logger.info("✅ Analisi completata")
        return self.analyzed_data
    
    def _load_data(self, source_info: Dict) -> Any:
        """Carica i dati da fonte"""
        import pandas as pd
        
        source_type = source_info['type']
        path = source_info['path']
        
        if source_type == 'csv':
            return pd.read_csv(path)
        elif source_type == 'json':
            with open(path, 'r') as f:
                return json.load(f)
        elif source_type == 'ga4':
            # Importa da GA4 export
            return pd.read_csv(path)
        else:
            raise ValueError(f"Tipo sorgente non supportato: {source_type}")
    
    def generate_report(self, source_name: str, report_format: str = 'html') -> str:
        """
        Genera un report dettagliato
        
        Args:
            source_name: Nome della fonte dati
            report_format: Formato del report (html, pdf, markdown, json)
        
        Returns:
            Percorso al file report generato
        """
        if source_name not in self.analyzed_data:
            logger.error(f"❌ Nessuna analisi trovata per: {source_name}")
            return ""
        
        logger.info(f"📝 Generazione report per {source_name} in formato {report_format}")
        
        from reports.report_generator import ReportGenerator
        
        generator = ReportGenerator(report_format)
        report_path = generator.generate(
            source_name,
            self.analyzed_data[source_name],
            self.config
        )
        
        self.reports[source_name] = {
            'format': report_format,
            'path': report_path,
            'generated_at': datetime.now().isoformat()
        }
        
        logger.info(f"✅ Report generato: {report_path}")
        return report_path
    
    def generate_all_reports(self, report_formats: Optional[List[str]] = None) -> Dict[str, str]:
        """
        Genera report per tutte le analisi
        
        Args:
            report_formats: Lista di formati (default: config)
        
        Returns:
            Dizionario con percorsi report
        """
        formats = report_formats or self.config['report_format']
        
        report_paths = {}
        for source_name in self.analyzed_data.keys():
            for fmt in formats:
                path = self.generate_report(source_name, fmt)
                report_paths[f"{source_name}_{fmt}"] = path
        
        return report_paths
    
    def get_summary(self) -> Dict[str, Any]:
        """Ritorna un sommario dello stato dell'agente"""
        return {
            'timestamp': self.timestamp.isoformat(),
            'total_sources': len(self.data_sources),
            'analyzed_sources': len(self.analyzed_data),
            'generated_reports': len(self.reports),
            'data_sources': self.data_sources,
            'reports': self.reports
        }
    
    def export_results(self, format: str = 'json', output_path: Optional[str] = None) -> str:
        """
        Esporta i risultati
        
        Args:
            format: Formato esportazione (json, csv, etc.)
            output_path: Percorso output (opzionale)
        
        Returns:
            Percorso al file esportato
        """
        from exporters.data_exporter import DataExporter
        
        exporter = DataExporter(format)
        output_path = exporter.export(
            self.analyzed_data,
            output_path or self.config['output_dir']
        )
        
        logger.info(f"✅ Risultati esportati: {output_path}")
        return output_path


def main():
    """Funzione principale per esecuzione CLI"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Web Analytics Agent - Analisi web analytics automatizzata'
    )
    parser.add_argument('--config', type=str, help='File configurazione JSON')
    parser.add_argument('--data', type=str, help='Percorso file dati')
    parser.add_argument('--type', type=str, default='csv', help='Tipo dati (csv, json, ga4)')
    parser.add_argument('--output', type=str, help='Cartella output')
    parser.add_argument('--format', type=str, default='html', 
                       help='Formato report (html, pdf, markdown, json)')
    
    args = parser.parse_args()
    
    # Inizializza agente
    agent = WebAnalyticsAgent(args.config)
    
    # Aggiungi fonte dati se specificata
    if args.data:
        agent.add_data_source('main', args.type, args.data)
    
    # Analizza
    agent.analyze_all_sources()
    
    # Genera report
    for source_name in agent.analyzed_data.keys():
        agent.generate_report(source_name, args.format)
    
    # Mostra sommario
    print("\n" + "="*70)
    print("📊 WEB ANALYTICS AGENT - REPORT")
    print("="*70)
    print(json.dumps(agent.get_summary(), indent=2, default=str))
    print("="*70)


if __name__ == '__main__':
    main()
