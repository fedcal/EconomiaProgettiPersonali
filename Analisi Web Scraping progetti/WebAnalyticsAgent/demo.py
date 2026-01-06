"""
Demo Script - Dimostra l'utilizzo dell'agente
"""

import sys
import os
from pathlib import Path
import pandas as pd
import json
from datetime import datetime, timedelta

# Aggiungi il percorso
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from web_analytics_agent import WebAnalyticsAgent


def create_sample_data(filename='sample_analytics.csv'):
    """Crea dati di esempio per il test"""
    print("📊 Creazione dati di esempio...")
    
    # Genera dati di esempio
    data = []
    base_date = datetime(2026, 1, 1)
    
    for i in range(100):
        date = base_date + timedelta(hours=i)
        data.append({
            'timestamp': date.isoformat(),
            'date': date.date(),
            'hour': date.hour,
            'sessions': 50 + (i % 30),
            'users': 40 + (i % 25),
            'pageviews': 150 + (i % 100),
            'bounced': i % 3,  # 0 or 1
            'converted': i % 15,  # 0 or 1
            'session_duration': 120 + (i % 60),
            'page': f"/page_{i % 10}",
            'source': ['organic', 'social', 'direct', 'email'][i % 4],
            'device_type': ['desktop', 'mobile', 'tablet'][i % 3],
            'browser': ['Chrome', 'Firefox', 'Safari'][i % 3],
            'country': ['Italy', 'USA', 'Germany'][i % 3],
            'conversion_value': (100 if i % 15 == 0 else 0)
        })
    
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)
    
    print(f"✅ Dati di esempio creati: {filename}")
    print(f"   - {len(df)} record")
    print(f"   - {len(df.columns)} colonne")
    
    return filename


def demo_basic_analysis():
    """Demo: Analisi base"""
    print("\n" + "="*70)
    print("DEMO 1: Analisi Base")
    print("="*70)
    
    # Crea dati di esempio
    data_file = create_sample_data('./data/sample_analytics.csv')
    
    # Inizializza agente
    agent = WebAnalyticsAgent('./config.json')
    
    # Aggiungi fonte dati
    agent.add_data_source('demo_site', 'csv', data_file)
    
    # Analizza
    print("\n🔍 Analisi in corso...\n")
    results = agent.analyze_all_sources()
    
    # Mostra risultati
    print("\n📊 Risultati Analisi:\n")
    
    if 'demo_site' in results:
        analysis = results['demo_site']['analysis']
        
        print("Traffic Analysis:")
        traffic = analysis.get('traffic', {})
        print(f"  - Total Sessions: {traffic.get('total_sessions', 0)}")
        print(f"  - Bounce Rate: {traffic.get('bounce_rate', 0):.2f}%")
        print(f"  - Avg Duration: {traffic.get('avg_session_duration', 0):.0f}s")
        
        print("\nUser Analysis:")
        users = analysis.get('users', {})
        print(f"  - Total Users: {users.get('total_users', 0)}")
        
        print("\nConversion Analysis:")
        conversions = analysis.get('conversions', {})
        print(f"  - Total Conversions: {conversions.get('total_conversions', 0)}")
        print(f"  - Conversion Rate: {conversions.get('conversion_rate', 0):.2f}%")


def demo_report_generation():
    """Demo: Generazione report"""
    print("\n" + "="*70)
    print("DEMO 2: Generazione Report")
    print("="*70)
    
    # Crea dati di esempio
    data_file = create_sample_data('./data/sample_analytics.csv')
    
    # Inizializza agente
    agent = WebAnalyticsAgent('./config.json')
    agent.add_data_source('demo_site', 'csv', data_file)
    
    # Analizza
    print("\n🔍 Analisi in corso...\n")
    agent.analyze_all_sources()
    
    # Genera report in diversi formati
    print("📝 Generazione report...\n")
    
    formats = ['html', 'markdown', 'json']
    for fmt in formats:
        try:
            report_path = agent.generate_report('demo_site', fmt)
            print(f"  ✅ {fmt.upper()}: {report_path}")
        except Exception as e:
            print(f"  ⚠️  {fmt.upper()}: {e}")


def demo_data_export():
    """Demo: Esportazione dati"""
    print("\n" + "="*70)
    print("DEMO 3: Esportazione Dati")
    print("="*70)
    
    # Crea dati di esempio
    data_file = create_sample_data('./data/sample_analytics.csv')
    
    # Inizializza agente
    agent = WebAnalyticsAgent('./config.json')
    agent.add_data_source('demo_site', 'csv', data_file)
    
    # Analizza
    print("\n🔍 Analisi in corso...\n")
    agent.analyze_all_sources()
    
    # Esporta
    print("📤 Esportazione...\n")
    
    try:
        json_path = agent.export_results('json', './exports')
        print(f"  ✅ JSON: {json_path}")
    except Exception as e:
        print(f"  ⚠️  JSON: {e}")


def demo_interactive():
    """Demo: Modo interattivo"""
    print("\n" + "="*70)
    print("DEMO 4: Modo Interattivo")
    print("="*70)
    
    print("\nEseguire:")
    print("  python cli.py --interactive")


def main():
    """Funzione principale"""
    print("\n" + "="*70)
    print("🤖 WEB ANALYTICS AGENT - DEMO")
    print("="*70 + "\n")
    
    print("Seleziona una demo:\n")
    print("1. Analisi Base")
    print("2. Generazione Report")
    print("3. Esportazione Dati")
    print("4. Informazioni Modo Interattivo")
    print("0. Esci\n")
    
    try:
        choice = input("Scelta (0-4): ").strip()
        
        if choice == '1':
            demo_basic_analysis()
        elif choice == '2':
            demo_report_generation()
        elif choice == '3':
            demo_data_export()
        elif choice == '4':
            demo_interactive()
        elif choice == '0':
            print("👋 Arrivederci!")
            return
        else:
            print("❌ Scelta non valida")
        
        # Sommario finale
        print("\n" + "="*70)
        print("✅ DEMO COMPLETATA")
        print("="*70)
        print("\nProssimi passi:")
        print("1. Posiziona i tuoi dati in ./data/")
        print("2. Esegui: python cli.py --data ./data/your_file.csv")
        print("3. Oppure usa modalità interattiva: python cli.py --interactive")
        print("\n")
    
    except KeyboardInterrupt:
        print("\n\n👋 Arrivederci!")


if __name__ == '__main__':
    main()
