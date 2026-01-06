"""
Script di elaborazione dati per PlayTheEvent
Pulisce, analizza e prepara i dati per la dashboard
"""

import pandas as pd
import numpy as np
from datetime import datetime
import json
import warnings

warnings.filterwarnings('ignore')

class DataProcessor:
    def __init__(self, csv_file):
        """Inizializza il processore dati"""
        self.df = None
        self.original_df = None
        self.load_data(csv_file)
    
    def load_data(self, csv_file):
        """Carica i dati dal CSV"""
        try:
            print(f"Caricamento dati da {csv_file}...")
            self.df = pd.read_csv(csv_file)
            self.original_df = self.df.copy()
            print(f"✓ Caricati {len(self.df)} record con {len(self.df.columns)} colonne")
            self.clean_data()
            self.analyze_data()
        except Exception as e:
            print(f"✗ Errore nel caricamento: {e}")
            raise
    
    def clean_data(self):
        """Pulisce i dati"""
        print("\nPulizia dati...")
        
        # Converti le colonne date
        if 'event_date' in self.df.columns:
            self.df['event_date'] = pd.to_datetime(self.df['event_date'], errors='coerce')
        
        if 'event_time' in self.df.columns:
            self.df['event_time'] = pd.to_datetime(self.df['event_time'], errors='coerce')
        
        # Estrai informazioni temporali
        if 'event_time' in self.df.columns:
            self.df['hour'] = self.df['event_time'].dt.hour
            self.df['day_of_week'] = self.df['event_time'].dt.day_name()
        
        # Rimuovi valori nulli da colonne critiche
        initial_rows = len(self.df)
        self.df = self.df.dropna(subset=['event_name'])
        print(f"✓ Rimossi {initial_rows - len(self.df)} record con event_name nullo")
    
    def analyze_data(self):
        """Analizza i dati"""
        print("\nAnalisi dati:")
        
        stats = {
            'Total Events': len(self.df),
            'Unique Users': self.df['user_pseudo_id'].nunique() if 'user_pseudo_id' in self.df.columns else 0,
            'Unique Sessions': self.df['ga_session_id'].nunique() if 'ga_session_id' in self.df.columns else 0,
            'Event Types': self.df['event_name'].nunique() if 'event_name' in self.df.columns else 0,
            'Countries': self.df['country'].nunique() if 'country' in self.df.columns else 0,
            'Cities': self.df['city'].nunique() if 'city' in self.df.columns else 0,
        }
        
        for key, value in stats.items():
            print(f"  • {key}: {value:,}")
        
        return stats
    
    def get_event_distribution(self):
        """Ritorna distribuzione degli eventi"""
        if 'event_name' not in self.df.columns:
            return pd.DataFrame()
        return self.df['event_name'].value_counts()
    
    def get_daily_events(self):
        """Ritorna eventi per giorno"""
        if 'event_date' not in self.df.columns:
            return pd.DataFrame()
        return self.df.groupby('event_date').size()
    
    def get_hourly_distribution(self):
        """Ritorna distribuzione oraria"""
        if 'hour' not in self.df.columns:
            return pd.DataFrame()
        return self.df['hour'].value_counts().sort_index()
    
    def get_geographic_distribution(self):
        """Ritorna distribuzione geografica"""
        geo_stats = {}
        
        if 'country' in self.df.columns:
            geo_stats['Countries'] = self.df['country'].value_counts()
        
        if 'city' in self.df.columns:
            geo_stats['Cities'] = self.df['city'].value_counts()
        
        if 'continent' in self.df.columns:
            geo_stats['Continents'] = self.df['continent'].value_counts()
        
        return geo_stats
    
    def get_device_stats(self):
        """Ritorna statistiche dispositivi"""
        device_stats = {}
        
        if 'operating_system' in self.df.columns:
            device_stats['Operating Systems'] = self.df['operating_system'].value_counts()
        
        if 'browser' in self.df.columns:
            device_stats['Browsers'] = self.df['browser'].value_counts()
        
        if 'language' in self.df.columns:
            device_stats['Languages'] = self.df['language'].value_counts()
        
        return device_stats
    
    def get_traffic_sources(self):
        """Ritorna sorgenti di traffic"""
        sources = {}
        
        if 'ts_source' in self.df.columns:
            sources['Source'] = self.df['ts_source'].value_counts()
        
        if 'ts_medium' in self.df.columns:
            sources['Medium'] = self.df['ts_medium'].value_counts()
        
        if 'ts_campaign' in self.df.columns:
            sources['Campaign'] = self.df['ts_campaign'].value_counts()
        
        return sources
    
    def get_user_engagement(self):
        """Ritorna statistiche di engagement"""
        engagement = {}
        
        if 'engagement_time_msec' in self.df.columns:
            engagement['avg_engagement_time'] = self.df['engagement_time_msec'].mean()
            engagement['max_engagement_time'] = self.df['engagement_time_msec'].max()
            engagement['total_engagement_time'] = self.df['engagement_time_msec'].sum()
        
        if 'session_engaged' in self.df.columns:
            engagement['engaged_sessions'] = self.df[self.df['session_engaged'] == 1].shape[0]
            engagement['engagement_rate'] = (engagement.get('engaged_sessions', 0) / len(self.df)) * 100 if len(self.df) > 0 else 0
        
        return engagement
    
    def export_summary(self, output_file='data_summary.json'):
        """Esporta un sommario dei dati"""
        print(f"\nEsportazione sommario in {output_file}...")
        
        summary = {
            'timestamp': datetime.now().isoformat(),
            'basic_stats': {
                'total_events': len(self.df),
                'unique_users': int(self.df['user_pseudo_id'].nunique()) if 'user_pseudo_id' in self.df.columns else 0,
                'unique_sessions': int(self.df['ga_session_id'].nunique()) if 'ga_session_id' in self.df.columns else 0,
                'event_types': int(self.df['event_name'].nunique()) if 'event_name' in self.df.columns else 0,
            },
            'geographic': {
                'countries': int(self.df['country'].nunique()) if 'country' in self.df.columns else 0,
                'cities': int(self.df['city'].nunique()) if 'city' in self.df.columns else 0,
            },
            'top_events': self.get_event_distribution().head(10).to_dict(),
            'device_info': {
                'os_count': int(self.df['operating_system'].nunique()) if 'operating_system' in self.df.columns else 0,
                'browser_count': int(self.df['browser'].nunique()) if 'browser' in self.df.columns else 0,
            }
        }
        
        with open(output_file, 'w') as f:
            json.dump(summary, f, indent=2, default=str)
        
        print(f"✓ Sommario esportato in {output_file}")
    
    def generate_report(self, output_file='data_analysis_report.md'):
        """Genera un report in markdown"""
        print(f"\nGenerazione report in {output_file}...")
        
        report = f"""# PlayTheEvent Data Analysis Report
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Executive Summary

### Key Metrics
- **Total Events**: {len(self.df):,}
- **Unique Users**: {self.df['user_pseudo_id'].nunique() if 'user_pseudo_id' in self.df.columns else 0:,}
- **Unique Sessions**: {self.df['ga_session_id'].nunique() if 'ga_session_id' in self.df.columns else 0:,}
- **Event Types**: {self.df['event_name'].nunique() if 'event_name' in self.df.columns else 0}

## Event Distribution

### Top 10 Events
"""
        
        top_events = self.get_event_distribution().head(10)
        for event, count in top_events.items():
            report += f"- {event}: {count:,}\n"
        
        report += f"""
## Geographic Analysis

### Top Countries
"""
        
        if 'country' in self.df.columns:
            top_countries = self.df['country'].value_counts().head(10)
            for country, count in top_countries.items():
                report += f"- {country}: {count:,}\n"
        
        report += f"""
## Traffic Sources

### Primary Source
"""
        
        if 'ts_source' in self.df.columns:
            sources = self.df['ts_source'].value_counts()
            for source, count in sources.items():
                report += f"- {source}: {count:,}\n"
        
        report += f"""
## Device Analysis

### Operating Systems
"""
        
        if 'operating_system' in self.df.columns:
            os_data = self.df['operating_system'].value_counts()
            for os, count in os_data.items():
                percentage = (count / len(self.df)) * 100
                report += f"- {os}: {count:,} ({percentage:.1f}%)\n"
        
        report += f"""
### Top Browsers
"""
        
        if 'browser' in self.df.columns:
            browsers = self.df['browser'].value_counts().head(10)
            for browser, count in browsers.items():
                percentage = (count / len(self.df)) * 100
                report += f"- {browser}: {count:,} ({percentage:.1f}%)\n"
        
        with open(output_file, 'w') as f:
            f.write(report)
        
        print(f"✓ Report esportato in {output_file}")

def main():
    """Funzione principale"""
    import sys
    
    csv_file = sys.argv[1] if len(sys.argv) > 1 else 'estrazione05012026.csv'
    
    try:
        processor = DataProcessor(csv_file)
        processor.export_summary()
        processor.generate_report()
        print("\n✓ Elaborazione completata!")
    except Exception as e:
        print(f"\n✗ Errore: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
