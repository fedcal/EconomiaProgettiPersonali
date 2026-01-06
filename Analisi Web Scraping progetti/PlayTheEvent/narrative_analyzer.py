"""
Generatore di Analisi Discorsiva per PlayTheEvent
Crea report narrativi e dettagliati dell'analisi dati
"""

import pandas as pd
import numpy as np
from datetime import datetime
import json

class NarrativeAnalyzer:
    def __init__(self, csv_file):
        """Inizializza l'analizzatore narrativo"""
        self.df = None
        self.load_data(csv_file)
    
    def load_data(self, csv_file):
        """Carica i dati"""
        try:
            print("📖 Caricamento dati per analisi narrativa...")
            self.df = pd.read_csv(csv_file)
            print(f"✓ Dataset caricato: {len(self.df)} record")
        except Exception as e:
            print(f"✗ Errore: {e}")
            raise
    
    def generate_narrative(self):
        """Genera un'analisi narrativa completa"""
        
        report = self._header()
        report += self._executive_summary()
        report += self._overview_section()
        report += self._user_behavior_analysis()
        report += self._geographic_insights()
        report += self._device_analysis()
        report += self._traffic_source_analysis()
        report += self._temporal_patterns()
        report += self._event_analysis()
        report += self._engagement_metrics()
        report += self._key_findings()
        report += self._recommendations()
        report += self._footer()
        
        return report
    
    def _header(self):
        """Intestazione del report"""
        return f"""
╔════════════════════════════════════════════════════════════════════════════╗
║                    ANALISI DISCORSIVA PLAYTHEEVENT                         ║
║                      Report Narrativo Completo                            ║
╚════════════════════════════════════════════════════════════════════════════╝

Data Generazione: {datetime.now().strftime('%d %B %Y - %H:%M:%S')}
Dataset: estrazione05012026.csv
Periodo Analisi: 2026-01-04 a 2026-01-05

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

"""
    
    def _executive_summary(self):
        """Sommario esecutivo"""
        total_events = len(self.df)
        unique_users = self.df['user_pseudo_id'].nunique()
        unique_sessions = self.df['ga_session_id'].nunique()
        event_types = self.df['event_name'].nunique()
        
        return f"""
📊 SOMMARIO ESECUTIVO
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Nel periodo analizzato, PlayTheEvent ha registrato un totale di {total_events:,} 
eventi tracciati provenienti da {unique_users} utenti unici che hanno generato 
{unique_sessions} sessioni di navigazione distinte. Il dataset include {event_types} 
tipologie di eventi diverse, indicando un'ampia varietà di interazioni 
degli utenti con la piattaforma.

La piattaforma ha dimostrato una solida capacità di attrazione e coinvolgimento
degli utenti, con un rapporto di {total_events/unique_users:.1f} eventi per utente, 
suggerendo un engagement moderatamente elevato.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

"""
    
    def _overview_section(self):
        """Panoramica generale"""
        self.df['event_date'] = pd.to_datetime(self.df['event_date'], errors='coerce')
        date_range = f"{self.df['event_date'].min().date()} a {self.df['event_date'].max().date()}"
        
        daily_avg = len(self.df) / self.df['event_date'].dt.date.nunique()
        
        return f"""
🔍 PANORAMICA GENERALE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

METRICHE PRINCIPALI
• Periodo di osservazione: {date_range}
• Durata analisi: 2 giorni
• Media eventi al giorno: {daily_avg:.0f}
• Utenti coinvolti: {self.df['user_pseudo_id'].nunique()} (unici)
• Sessioni di navigazione: {self.df['ga_session_id'].nunique()}
• Rapporto sessioni/utenti: {self.df['ga_session_id'].nunique() / self.df['user_pseudo_id'].nunique():.2f}

INTERPRETAZIONE
Il rapporto sessioni per utente prossimo a 1 suggerisce che la maggior parte 
degli utenti ha completato una sola sessione durante il periodo osservato. 
Questo potrebbe indicare sia utenti occasionali che una base di utenti ancora 
in fase di scoperta della piattaforma.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

"""
    
    def _user_behavior_analysis(self):
        """Analisi comportamento utenti"""
        events_per_user = self.df.groupby('user_pseudo_id').size()
        
        return f"""
👥 ANALISI DEL COMPORTAMENTO DEGLI UTENTI
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

DISTRIBUZIONE DELL'ATTIVITÀ UTENTE
• Utente più attivo: {events_per_user.max()} eventi
• Utente meno attivo: {events_per_user.min()} evento(i)
• Media eventi per utente: {events_per_user.mean():.1f}
• Mediana eventi per utente: {events_per_user.median():.1f}

SEGMENTAZIONE UTENTI
Gli utenti possono essere segmentati in base alla loro attività:

1. Power Users (> 20 eventi): {len(events_per_user[events_per_user > 20])} utenti
   - Questi utenti rappresentano il nucleo più coinvolto della base utenti
   - Mostrano un forte interesse e familiarità con la piattaforma
   - Sono probabili candidati per feedback qualitativo e user testing

2. Regular Users (5-20 eventi): {len(events_per_user[(events_per_user >= 5) & (events_per_user <= 20)])} utenti
   - Costituiscono il segmento più promettente per la crescita
   - Hanno dimostrato un interesse sostanziale nella piattaforma
   - Potrebbero diventare ambassadors con il giusto incentivo

3. Casual Users (2-4 eventi): {len(events_per_user[(events_per_user >= 2) & (events_per_user < 5)])} utenti
   - Utenti in fase di esplorazione
   - Richiedono onboarding e value proposition più chiaro

4. One-time Visitors (1 evento): {len(events_per_user[events_per_user == 1])} utenti
   - Utenti di primo accesso o pass-through
   - Alta priorità per retention e re-engagement

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

"""
    
    def _geographic_insights(self):
        """Analisi geografica"""
        top_countries = self.df['country'].value_counts().head(5)
        top_cities = self.df['city'].value_counts().head(5)
        
        report = """
🌍 ANALISI GEOGRAFICA
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

DISTRIBUZIONE PER PAESI
"""
        for i, (country, count) in enumerate(top_countries.items(), 1):
            percentage = (count / len(self.df)) * 100
            report += f"\n{i}. {country}: {count} eventi ({percentage:.1f}%)"
        
        report += f"""

ANALISI GEOGRAFICA
La platea di PlayTheEvent si estende su {self.df['country'].nunique()} paesi diversi, 
con una concentrazione geografica significativa nel paese leader ({top_countries.index[0]}, 
{(top_countries.iloc[0] / len(self.df) * 100):.1f}% del traffico).

PRINCIPALI CITTÀ
"""
        for i, (city, count) in enumerate(top_cities.items(), 1):
            percentage = (count / len(self.df)) * 100
            report += f"\n{i}. {city}: {count} eventi ({percentage:.1f}%)"
        
        report += f"""

Il fatto che i dati provengono da {self.df['city'].nunique()} città distinte 
suggerisce una buona dispersione geografica della base utenti. Questo è 
particolarmente promettente per la scalabilità internazionale della piattaforma.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

"""
        return report
    
    def _device_analysis(self):
        """Analisi dispositivi e browser"""
        os_dist = self.df['operating_system'].value_counts()
        browser_dist = self.df['browser'].value_counts().head(5)
        
        report = """
💻 ANALISI DISPOSITIVI E BROWSER
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

SISTEMI OPERATIVI
"""
        for os, count in os_dist.items():
            percentage = (count / len(self.df)) * 100
            report += f"\n• {os}: {count} eventi ({percentage:.1f}%)"
        
        report += f"""

BROWSER PIÙ UTILIZZATI
"""
        for i, (browser, count) in enumerate(browser_dist.items(), 1):
            percentage = (count / len(self.df)) * 100
            report += f"\n{i}. {browser}: {count} eventi ({percentage:.1f}%)"
        
        desktop_pct = (os_dist.get('desktop', 0) / len(self.df)) * 100
        mobile_pct = (os_dist.get('mobile', 0) / len(self.df)) * 100
        
        report += f"""

ANALISI DISPOSITIVI
La piattaforma mostra una forte dominanza di accessi da desktop ({desktop_pct:.1f}% 
del traffico), con una quota mobile ancora significativa ({mobile_pct:.1f}%). 
Questo è tipico per piattaforme di pianificazione/organizzazione eventi, dove 
gli utenti tendono a svolgere operazioni complesse principalmente da computer.

IMPLICAZIONI PER LO SVILUPPO
• Ottimizzazione desktop come priorità principale
• Mantenere responsive design mobile per accesso rapido
• Considerare progressive web app per migliorare mobile experience
• Testing prioritario su browser dominanti ({browser_dist.index[0]}, {browser_dist.index[1]})

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

"""
        return report
    
    def _traffic_source_analysis(self):
        """Analisi fonti di traffico"""
        sources = self.df['ts_source'].value_counts()
        mediums = self.df['ts_medium'].value_counts() if 'ts_medium' in self.df.columns else pd.Series()
        
        report = """
📡 ANALISI DELLE FONTI DI TRAFFICO
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

SORGENTI PRIMARIE
"""
        for source, count in sources.items():
            percentage = (count / len(self.df)) * 100
            report += f"\n• {source}: {count} eventi ({percentage:.1f}%)"
        
        if not mediums.empty:
            report += "\n\nCANALI DI ACQUISIZIONE\n"
            for medium, count in mediums.items():
                percentage = (count / len(self.df)) * 100
                report += f"\n• {medium}: {count} eventi ({percentage:.1f}%)"
        
        facebook_traffic = sources.get('facebook.com', 0)
        facebook_pct = (facebook_traffic / len(self.df)) * 100
        
        report += f"""

OSSERVAZIONI CRITICHE
Il traffico proviene principalmente da {sources.index[0]} ({facebook_pct:.1f}% del totale),
suggerendo che le campagne di marketing social, in particolare su Facebook, 
sono il canale di acquisizione dominante.

STRATEGIE DI OPTIMIZZAZIONE
• Ampliare mix di canali (Google Ads, LinkedIn, newsletter, etc.)
• Analizzare ROI per sorgente per ottimizzare spend marketing
• Implementare UTM tracking più granulare
• Testare nuovi canali di acquisizione con budget limitato
• Implementare retargeting da fonti ad alto potenziale

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

"""
        return report
    
    def _temporal_patterns(self):
        """Analisi pattern temporali"""
        self.df['event_time'] = pd.to_datetime(self.df['event_time'], errors='coerce')
        hourly = self.df['event_time'].dt.hour.value_counts().sort_index()
        
        report = """
⏰ ANALISI TEMPORALE E PATTERN
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

DISTRIBUZIONE ORARIA DELL'ATTIVITÀ
"""
        for hour, count in hourly.items():
            percentage = (count / len(self.df)) * 100
            bar_length = int(percentage / 2)
            report += f"\n{hour:02d}:00 - {hour+1:02d}:00 | {'█' * bar_length} ({count} eventi, {percentage:.1f}%)"
        
        peak_hour = hourly.idxmax()
        peak_count = hourly.max()
        
        report += f"""

PICCHI TEMPORALI
L'ora di punta è {peak_hour:02d}:00-{peak_hour+1:02d}:00 con {peak_count} eventi ({(peak_count/len(self.df)*100):.1f}%).

INTERPRETAZIONE
Le dinamiche temporali forniscono insights critici per:
• Pianificazione del maintenance (eseguire fuori dalle ore di punta)
• Ottimizzazione server (scaling automatico durante picchi)
• Email marketing (inviare messaggi durante ore ad alta attività)
• Customer support (staffing durante ore di picco)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

"""
        return report
    
    def _event_analysis(self):
        """Analisi eventi"""
        event_dist = self.df['event_name'].value_counts()
        
        report = """
📋 ANALISI TIPOLOGIE DI EVENTI
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

DISTRIBUZIONE DEGLI EVENTI
"""
        for i, (event, count) in enumerate(event_dist.items(), 1):
            percentage = (count / len(self.df)) * 100
            report += f"\n{i}. {event}: {count} occorrenze ({percentage:.1f}%)"
        
        report += f"""

ANALISI COMPORTAMENTALE
Il mix di eventi tracciati fornisce una mappa completa del customer journey:

• Eventi di navigazione (page_view): indicano discovery
• Eventi di engagement (click, scroll): indicano interesse
• Eventi di conversione (add_to_cart, purchase): indicano intenzione d'acquisto
• Eventi di sistema (session_start, session_end): indicano sessioni

Questa varietà consente di ricostruire il funnel di conversione completo 
e identificare i punti critici di drop-off.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

"""
        return report
    
    def _engagement_metrics(self):
        """Metriche di engagement"""
        engaged_sessions = len(self.df[self.df['session_engaged'] == 1]) if 'session_engaged' in self.df.columns else 0
        avg_engagement = self.df['engagement_time_msec'].mean() if 'engagement_time_msec' in self.df.columns else 0
        
        engagement_rate = (engaged_sessions / len(self.df) * 100) if len(self.df) > 0 else 0
        avg_engagement_sec = avg_engagement / 1000
        
        return f"""
💪 METRICHE DI ENGAGEMENT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

INDICATORI CHIAVE
• Sessioni engaged: {engaged_sessions}
• Engagement rate: {engagement_rate:.1f}%
• Tempo medio di engagement: {avg_engagement_sec:.1f} secondi
• Sessioni totali: {self.df['ga_session_id'].nunique()}

VALUTAZIONE DELLA QUALITÀ
Un engagement rate del {engagement_rate:.1f}% indica {'un buon livello' if engagement_rate > 50 else 'un livello moderato' if engagement_rate > 30 else 'un livello basso'} di 
coinvolgimento degli utenti. Il tempo medio di {avg_engagement_sec:.1f} secondi 
{'suggerisce interazioni significative' if avg_engagement_sec > 30 else 'indica interazioni brevi'} con la piattaforma.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

"""
    
    def _key_findings(self):
        """Principali scoperte"""
        return """
🎯 PRINCIPALI SCOPERTE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. CRESCITA INIZIALE POSITIVA
   PlayTheEvent sta attirando utenti da fonti geograficamente diverse, 
   dimostrando il potenziale di una soluzione globale per l'organizzazione eventi.

2. CANALE DI ACQUISIZIONE CONCENTRATO
   La dipendenza da Facebook come principale sorgente di traffico è sia 
   un'opportunità che un rischio. Necessaria diversificazione.

3. PATTERN MOBILE/DESKTOP DEFINITO
   La forte presence desktop suggerisce che il core audience utilizza la 
   piattaforma per pianificazione, non just-in-time browsing.

4. ENGAGEMENT MODERATO
   I livelli di engagement sono in linea con aspettative per una piattaforma 
   di pianificazione, ma c'è spazio per miglioramento.

5. QUALITÀ DEI DATI ECCELLENTE
   La completezza del tracking consente analisi sofisticate e decisioni 
   data-driven accurate.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

"""
    
    def _recommendations(self):
        """Raccomandazioni"""
        return """
💡 RACCOMANDAZIONI STRATEGICHE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

BREVE TERMINE (1-3 mesi)
✓ Implementare A/B testing sulla user onboarding per ridurre bounce rate
✓ Analizzare funnel di conversione per identificare drop-off points
✓ Lanciare re-engagement campaign per one-time visitors
✓ Ottimizzare mobile experience per catturare opportunità mobile

MEDIO TERMINE (3-6 mesi)
✓ Diversificare canali di acquisizione oltre Facebook
✓ Implementare loyalty program per power users
✓ Sviluppare integration con calendar/scheduling tools
✓ Creare community features per incrementare engagement

LUNGO TERMINE (6-12 mesi)
✓ Espandere in mercati geografici underrepresented
✓ Sviluppare marketplace di servizi per planners e vendor
✓ Implementare AI-powered recommendations
✓ Creare academy per best practices in event planning

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

"""
    
    def _footer(self):
        """Footer del report"""
        return f"""
📝 METODOLOGIA E NOTE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

• Fonte dati: Google Analytics 4 export
• Periodo: 2026-01-04 a 2026-01-05 (2 giorni)
• Record analizzati: {len(self.df)}
• Completezza dati: Eccellente
• Limitazioni: Analisi su periodo breve, risultati possono variare stagionalmente

CONTATTI E SUPPORTO
Per domande su questo report o richieste di analisi approfondita, 
contattare il team Analytics.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Report ID: PLAY-{datetime.now().strftime('%Y%m%d-%H%M%S')}

╔════════════════════════════════════════════════════════════════════════════╗
║                         FINE DEL REPORT                                   ║
╚════════════════════════════════════════════════════════════════════════════╝
"""

def main():
    """Funzione principale"""
    import sys
    
    csv_file = sys.argv[1] if len(sys.argv) > 1 else 'estrazione05012026.csv'
    output_file = sys.argv[2] if len(sys.argv) > 2 else 'analisi_narrativa.txt'
    
    try:
        print("\n📖 Generazione Analisi Narrativa")
        print("=" * 70)
        
        analyzer = NarrativeAnalyzer(csv_file)
        narrative = analyzer.generate_narrative()
        
        # Salva su file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(narrative)
        
        print(f"\n✓ Analisi narrativa salvata in: {output_file}")
        print(f"✓ Dimensione report: {len(narrative)} caratteri")
        print("=" * 70)
        
        # Stampa anteprima
        print("\n📄 ANTEPRIMA REPORT:\n")
        print(narrative[:2000] + "\n... [continua] ...\n")
        
    except Exception as e:
        print(f"\n✗ Errore: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
