#!/usr/bin/env python3
"""
Main CLI Interface - Interfaccia CLI per l'agente
"""

import argparse
import sys
import os
from pathlib import Path

# Aggiungi la cartella al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from web_analytics_agent import WebAnalyticsAgent
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    """Funzione principale CLI"""
    parser = argparse.ArgumentParser(
        description='🤖 Web Analytics Agent - Agente autonomo di analisi web analytics',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Esempi di uso:

  # Analizza un file CSV
  python cli.py --data data.csv --type csv --format html

  # Analizza più file
  python cli.py --data data1.csv data2.csv --type csv --format all

  # Usa configurazione personalizzata
  python cli.py --config config.json --data data.csv

  # Esporta i risultati
  python cli.py --data data.csv --export json
        """
    )
    
    parser.add_argument(
        '--data', 
        type=str, 
        nargs='+',
        help='Percorso ai file dati'
    )
    
    parser.add_argument(
        '--type',
        type=str,
        default='csv',
        choices=['csv', 'json', 'ga4', 'log'],
        help='Tipo di dati'
    )
    
    parser.add_argument(
        '--config',
        type=str,
        help='File configurazione JSON'
    )
    
    parser.add_argument(
        '--output',
        type=str,
        default='./reports',
        help='Cartella output'
    )
    
    parser.add_argument(
        '--format',
        type=str,
        default='html',
        choices=['html', 'markdown', 'json', 'pdf', 'all'],
        help='Formato report'
    )
    
    parser.add_argument(
        '--export',
        type=str,
        choices=['json', 'csv'],
        help='Esporta risultati in formato'
    )
    
    parser.add_argument(
        '--interactive',
        action='store_true',
        help='Modalità interattiva'
    )
    
    args = parser.parse_args()
    
    # Inizializza agente
    print("\n" + "="*70)
    print("🤖 WEB ANALYTICS AGENT")
    print("="*70 + "\n")
    
    config_file = args.config or os.path.join(
        os.path.dirname(__file__), 
        'config.json'
    )
    
    agent = WebAnalyticsAgent(config_file)
    
    # Modalità interattiva
    if args.interactive:
        interactive_mode(agent)
        return
    
    # Modalità CLI
    if not args.data:
        parser.print_help()
        return
    
    # Aggiungi fonti dati
    for i, data_file in enumerate(args.data):
        source_name = f"source_{i+1}" if len(args.data) > 1 else "main"
        
        if not os.path.exists(data_file):
            logger.error(f"❌ File non trovato: {data_file}")
            continue
        
        agent.add_data_source(source_name, args.type, data_file)
    
    # Analizza
    print("🔍 Avvio analisi...\n")
    agent.analyze_all_sources()
    
    # Genera report
    print("\n📝 Generazione report...\n")
    formats = ['html', 'markdown', 'json', 'pdf'] if args.format == 'all' else [args.format]
    
    for source_name in agent.analyzed_data.keys():
        for fmt in formats:
            try:
                agent.generate_report(source_name, fmt)
            except Exception as e:
                logger.warning(f"⚠️  Non è stato possibile generare {fmt}: {e}")
    
    # Esporta
    if args.export:
        print(f"\n📤 Esportazione dati in {args.export}...\n")
        agent.export_results(args.export, args.output)
    
    # Sommario
    print("\n" + "="*70)
    print("✅ ANALISI COMPLETATA")
    print("="*70)
    print(json.dumps(agent.get_summary(), indent=2, default=str))
    print("="*70 + "\n")


def interactive_mode(agent):
    """Modalità interattiva"""
    print("📱 Modalità Interattiva")
    print("-" * 70)
    print("Comandi disponibili:")
    print("  add <name> <type> <path>  - Aggiungi fonte dati")
    print("  analyze                   - Analizza tutte le fonti")
    print("  report <source> <format>  - Genera report")
    print("  export <format>           - Esporta risultati")
    print("  status                    - Mostra stato")
    print("  help                      - Mostra aiuto")
    print("  exit                      - Esci")
    print("-" * 70 + "\n")
    
    while True:
        try:
            cmd = input(">>> ").strip().split()
            
            if not cmd:
                continue
            
            if cmd[0] == 'exit':
                print("👋 Arrivederci!")
                break
            
            elif cmd[0] == 'add' and len(cmd) >= 4:
                name, source_type, path = cmd[1], cmd[2], ' '.join(cmd[3:])
                agent.add_data_source(name, source_type, path)
            
            elif cmd[0] == 'analyze':
                agent.analyze_all_sources()
                print("✅ Analisi completata")
            
            elif cmd[0] == 'report' and len(cmd) >= 2:
                source = cmd[1]
                fmt = cmd[2] if len(cmd) > 2 else 'html'
                agent.generate_report(source, fmt)
                print(f"✅ Report {fmt} generato")
            
            elif cmd[0] == 'export' and len(cmd) >= 2:
                agent.export_results(cmd[1])
                print(f"✅ Dati esportati")
            
            elif cmd[0] == 'status':
                print(json.dumps(agent.get_summary(), indent=2, default=str))
            
            elif cmd[0] == 'help':
                print("Comandi disponibili: add, analyze, report, export, status, help, exit")
            
            else:
                print("❌ Comando non riconosciuto")
        
        except KeyboardInterrupt:
            print("\n👋 Arrivederci!")
            break
        except Exception as e:
            print(f"❌ Errore: {e}")


if __name__ == '__main__':
    main()
