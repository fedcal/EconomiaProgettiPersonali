"""
Dashboard interattiva per l'analisi dei dati di PlayTheEvent
Utilizza Dash e Plotly per visualizzazioni interattive
"""

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import dash
from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
from datetime import datetime, timedelta
import warnings

warnings.filterwarnings('ignore')

# Configurazione
DATA_FILE = 'estrazione05012026.csv'
THEME = dbc.themes.BOOTSTRAP

class DataAnalyzer:
    def __init__(self, csv_file):
        """Inizializza l'analizzatore con i dati da file CSV"""
        self.df = None
        self.load_data(csv_file)
    
    def load_data(self, csv_file):
        """Carica i dati dal file CSV"""
        try:
            print(f"Caricamento dati da {csv_file}...")
            self.df = pd.read_csv(csv_file)
            print(f"Dati caricati: {len(self.df)} righe, {len(self.df.columns)} colonne")
            self._prepare_data()
        except Exception as e:
            print(f"Errore nel caricamento dati: {e}")
    
    def _prepare_data(self):
        """Prepara i dati per l'analisi"""
        # Converti event_date a datetime se necessario
        if 'event_date' in self.df.columns:
            self.df['event_date'] = pd.to_datetime(self.df['event_date'], errors='coerce')
        
        # Converti event_time a datetime
        if 'event_time' in self.df.columns:
            self.df['event_time'] = pd.to_datetime(self.df['event_time'], errors='coerce')
        
        # Estrai ora dai dati temporali
        if 'event_time' in self.df.columns:
            self.df['hour'] = self.df['event_time'].dt.hour
    
    def get_summary_stats(self):
        """Ritorna statistiche riassuntive"""
        return {
            'Total Events': len(self.df),
            'Unique Users': self.df['user_pseudo_id'].nunique() if 'user_pseudo_id' in self.df.columns else 0,
            'Date Range': f"{self.df['event_date'].min().date()} to {self.df['event_date'].max().date()}" if 'event_date' in self.df.columns else 'N/A',
            'Event Types': self.df['event_name'].nunique() if 'event_name' in self.df.columns else 0
        }
    
    def get_events_by_type(self):
        """Ritorna conteggio degli eventi per tipo"""
        if 'event_name' not in self.df.columns:
            return pd.DataFrame()
        return self.df['event_name'].value_counts().head(15).reset_index()
    
    def get_events_by_date(self):
        """Ritorna evoluzione degli eventi nel tempo"""
        if 'event_date' not in self.df.columns:
            return pd.DataFrame()
        return self.df.groupby('event_date').size().reset_index(name='count')
    
    def get_events_by_hour(self):
        """Ritorna distribuzione eventi per ora del giorno"""
        if 'hour' not in self.df.columns:
            return pd.DataFrame()
        return self.df['hour'].value_counts().sort_index().reset_index()
    
    def get_top_countries(self):
        """Ritorna i paesi con più traffic"""
        if 'country' not in self.df.columns:
            return pd.DataFrame()
        return self.df['country'].value_counts().head(10).reset_index()
    
    def get_top_cities(self):
        """Ritorna le città con più traffic"""
        if 'city' not in self.df.columns:
            return pd.DataFrame()
        return self.df['city'].value_counts().head(10).reset_index()
    
    def get_device_stats(self):
        """Ritorna statistiche per dispositivo"""
        if 'operating_system' not in self.df.columns:
            return pd.DataFrame()
        return self.df['operating_system'].value_counts().reset_index()
    
    def get_browser_stats(self):
        """Ritorna statistiche per browser"""
        if 'browser' not in self.df.columns:
            return pd.DataFrame()
        return self.df['browser'].value_counts().head(10).reset_index()
    
    def get_traffic_sources(self):
        """Ritorna sorgenti di traffic"""
        if 'ts_source' not in self.df.columns:
            return pd.DataFrame()
        return self.df['ts_source'].value_counts().reset_index()

# Inizializza l'analizzatore
try:
    analyzer = DataAnalyzer(DATA_FILE)
except Exception as e:
    print(f"Errore nell'inizializzazione: {e}")
    analyzer = None

# Crea l'app Dash
app = dash.Dash(__name__, external_stylesheets=[THEME])
app.title = "PlayTheEvent Analytics Dashboard"

# Define il layout dell'app
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1("📊 PlayTheEvent Analytics Dashboard", className="mb-4 mt-4 text-center")
        ])
    ]),
    
    # Statistiche Riassuntive
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("Total Events", className="card-title"),
                    html.H2(id="total-events", children="0")
                ])
            ])
        ], md=3),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("Unique Users", className="card-title"),
                    html.H2(id="unique-users", children="0")
                ])
            ])
        ], md=3),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("Event Types", className="card-title"),
                    html.H2(id="event-types", children="0")
                ])
            ])
        ], md=3),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("Date Range", className="card-title"),
                    html.P(id="date-range", children="N/A", className="text-sm")
                ])
            ])
        ], md=3),
    ], className="mb-4"),
    
    # Grafici principali
    dbc.Row([
        dbc.Col([
            dcc.Graph(id="events-by-type-chart")
        ], md=6),
        dbc.Col([
            dcc.Graph(id="events-by-date-chart")
        ], md=6),
    ], className="mb-4"),
    
    # Grafici secondari
    dbc.Row([
        dbc.Col([
            dcc.Graph(id="events-by-hour-chart")
        ], md=6),
        dbc.Col([
            dcc.Graph(id="device-stats-chart")
        ], md=6),
    ], className="mb-4"),
    
    # Grafici geografici
    dbc.Row([
        dbc.Col([
            dcc.Graph(id="top-countries-chart")
        ], md=6),
        dbc.Col([
            dcc.Graph(id="traffic-sources-chart")
        ], md=6),
    ], className="mb-4"),
    
    # Browser e altre metriche
    dbc.Row([
        dbc.Col([
            dcc.Graph(id="browser-stats-chart")
        ], md=6),
        dbc.Col([
            dcc.Graph(id="top-cities-chart")
        ], md=6),
    ], className="mb-4"),
    
], fluid=True, className="bg-light")

# Callbacks per aggiornare i grafici
@app.callback(
    [Output("total-events", "children"),
     Output("unique-users", "children"),
     Output("event-types", "children"),
     Output("date-range", "children")],
    Input("events-by-type-chart", "id")
)
def update_summary(id):
    """Aggiorna le statistiche riassuntive"""
    if analyzer is None or analyzer.df is None:
        return "0", "0", "0", "N/A"
    
    stats = analyzer.get_summary_stats()
    return (stats['Total Events'], 
            stats['Unique Users'], 
            stats['Event Types'], 
            stats['Date Range'])

@app.callback(
    Output("events-by-type-chart", "figure"),
    Input("events-by-type-chart", "id")
)
def update_events_by_type(id):
    """Aggiorna il grafico degli eventi per tipo"""
    if analyzer is None or analyzer.df is None:
        return {}
    
    data = analyzer.get_events_by_type()
    if data.empty:
        return {}
    
    fig = px.bar(data, x='event_name', y='count', 
                 title='Top 15 Event Types',
                 labels={'count': 'Number of Events', 'event_name': 'Event Type'},
                 color='count', color_continuous_scale='Viridis')
    fig.update_layout(height=400, xaxis_tickangle=-45)
    return fig

@app.callback(
    Output("events-by-date-chart", "figure"),
    Input("events-by-date-chart", "id")
)
def update_events_by_date(id):
    """Aggiorna il grafico degli eventi nel tempo"""
    if analyzer is None or analyzer.df is None:
        return {}
    
    data = analyzer.get_events_by_date()
    if data.empty:
        return {}
    
    fig = px.line(data, x='event_date', y='count',
                  title='Events Over Time',
                  labels={'count': 'Number of Events', 'event_date': 'Date'},
                  markers=True)
    fig.update_layout(height=400)
    return fig

@app.callback(
    Output("events-by-hour-chart", "figure"),
    Input("events-by-hour-chart", "id")
)
def update_events_by_hour(id):
    """Aggiorna il grafico degli eventi per ora"""
    if analyzer is None or analyzer.df is None:
        return {}
    
    data = analyzer.get_events_by_hour()
    if data.empty:
        return {}
    
    fig = px.bar(data, x='hour', y='count',
                 title='Events Distribution by Hour of Day',
                 labels={'count': 'Number of Events', 'hour': 'Hour (UTC)'},
                 color='count', color_continuous_scale='Blues')
    fig.update_layout(height=400)
    return fig

@app.callback(
    Output("device-stats-chart", "figure"),
    Input("device-stats-chart", "id")
)
def update_device_stats(id):
    """Aggiorna il grafico delle statistiche dei dispositivi"""
    if analyzer is None or analyzer.df is None:
        return {}
    
    data = analyzer.get_device_stats()
    if data.empty:
        return {}
    
    fig = px.pie(data, values='count', names='operating_system',
                 title='Traffic by Operating System')
    fig.update_layout(height=400)
    return fig

@app.callback(
    Output("top-countries-chart", "figure"),
    Input("top-countries-chart", "id")
)
def update_top_countries(id):
    """Aggiorna il grafico dei paesi principali"""
    if analyzer is None or analyzer.df is None:
        return {}
    
    data = analyzer.get_top_countries()
    if data.empty:
        return {}
    
    fig = px.bar(data, x='count', y='country', orientation='h',
                 title='Top 10 Countries by Traffic',
                 labels={'count': 'Number of Events', 'country': 'Country'},
                 color='count', color_continuous_scale='Greens')
    fig.update_layout(height=400)
    return fig

@app.callback(
    Output("traffic-sources-chart", "figure"),
    Input("traffic-sources-chart", "id")
)
def update_traffic_sources(id):
    """Aggiorna il grafico delle sorgenti di traffic"""
    if analyzer is None or analyzer.df is None:
        return {}
    
    data = analyzer.get_traffic_sources()
    if data.empty:
        return {}
    
    fig = px.pie(data, values='count', names='ts_source',
                 title='Traffic Sources')
    fig.update_layout(height=400)
    return fig

@app.callback(
    Output("browser-stats-chart", "figure"),
    Input("browser-stats-chart", "id")
)
def update_browser_stats(id):
    """Aggiorna il grafico delle statistiche dei browser"""
    if analyzer is None or analyzer.df is None:
        return {}
    
    data = analyzer.get_browser_stats()
    if data.empty:
        return {}
    
    fig = px.bar(data, x='browser', y='count',
                 title='Top 10 Browsers',
                 labels={'count': 'Number of Events', 'browser': 'Browser'},
                 color='count', color_continuous_scale='Oranges')
    fig.update_layout(height=400, xaxis_tickangle=-45)
    return fig

@app.callback(
    Output("top-cities-chart", "figure"),
    Input("top-cities-chart", "id")
)
def update_top_cities(id):
    """Aggiorna il grafico delle città principali"""
    if analyzer is None or analyzer.df is None:
        return {}
    
    data = analyzer.get_top_cities()
    if data.empty:
        return {}
    
    fig = px.bar(data, x='count', y='city', orientation='h',
                 title='Top 10 Cities by Traffic',
                 labels={'count': 'Number of Events', 'city': 'City'},
                 color='count', color_continuous_scale='Reds')
    fig.update_layout(height=400)
    return fig

if __name__ == '__main__':
    print("🚀 Avvio dashboard su http://localhost:8050")
    print("Premi Ctrl+C per fermare il server")
    app.run_server(debug=True, host='0.0.0.0', port=8050)
