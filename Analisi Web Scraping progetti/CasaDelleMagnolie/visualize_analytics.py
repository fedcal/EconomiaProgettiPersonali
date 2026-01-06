#!/usr/bin/env python3
"""
Google Analytics Data Visualizer
Creates charts and graphs from analytics data
"""

import json
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta
from analytics_analyzer import GoogleAnalyticsParser


class AnalyticsVisualizer:
    """Create visualizations from analytics data."""

    def __init__(self, data: dict, summary: dict):
        self.data = data
        self.summary = summary
        plt.style.use('seaborn-v0_8-darkgrid')

    def create_all_charts(self, output_prefix="analytics"):
        """Create all visualization charts."""
        print("📊 Generazione grafici...")

        # 1. Daily users trend
        self.plot_daily_users(f"{output_prefix}_daily_users.png")

        # 2. Traffic sources pie chart
        self.plot_traffic_sources(f"{output_prefix}_traffic_sources.png")

        # 3. Geography bar chart
        self.plot_geography(f"{output_prefix}_geography.png")

        # 4. Top pages bar chart
        self.plot_top_pages(f"{output_prefix}_top_pages.png")

        # 5. User trends (30/7/1 day)
        self.plot_user_trends(f"{output_prefix}_user_trends.png")

        # 6. Events breakdown
        self.plot_events(f"{output_prefix}_events.png")

        print(f"✅ Grafici salvati!")

    def plot_daily_users(self, filename: str):
        """Plot daily active users over time."""
        daily_data = self.data['daily_active_users']

        if not daily_data:
            print(f"⚠️  Nessun dato per utenti giornalieri")
            return

        days = [d['day'] for d in daily_data]
        users = [d['value'] for d in daily_data]

        # Convert days to dates
        start_date = datetime.strptime(self.data['metadata']['start_date'], '%Y-%m-%d')
        dates = [start_date + timedelta(days=d) for d in days]

        fig, ax = plt.subplots(figsize=(12, 6))
        ax.plot(dates, users, marker='o', linewidth=2, markersize=6, color='#1f77b4')
        ax.fill_between(dates, users, alpha=0.3, color='#1f77b4')

        ax.set_xlabel('Data', fontsize=12)
        ax.set_ylabel('Utenti Attivi', fontsize=12)
        ax.set_title('Trend Utenti Attivi Giornalieri', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3)

        # Format x-axis
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m'))
        plt.xticks(rotation=45)

        plt.tight_layout()
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()

        print(f"  ✓ {filename}")

    def plot_traffic_sources(self, filename: str):
        """Plot traffic sources as pie chart."""
        sources = self.summary['traffic_sources']['new_users_by_source']

        if not sources:
            print(f"⚠️  Nessun dato per sorgenti traffico")
            return

        labels = list(sources.keys())
        sizes = list(sources.values())
        colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99', '#ff99cc']

        fig, ax = plt.subplots(figsize=(10, 8))
        wedges, texts, autotexts = ax.pie(
            sizes,
            labels=labels,
            colors=colors[:len(labels)],
            autopct='%1.1f%%',
            startangle=90,
            textprops={'fontsize': 11}
        )

        # Make percentage text bold
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')

        ax.set_title('Distribuzione Sorgenti Traffico (Nuovi Utenti)', fontsize=14, fontweight='bold')

        plt.tight_layout()
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()

        print(f"  ✓ {filename}")

    def plot_geography(self, filename: str):
        """Plot geographic distribution as bar chart."""
        countries = self.summary['geography']['countries']

        if not countries:
            print(f"⚠️  Nessun dato geografico")
            return

        # Sort by value
        sorted_countries = sorted(countries.items(), key=lambda x: x[1], reverse=True)
        labels = [c[0] for c in sorted_countries]
        values = [c[1] for c in sorted_countries]

        fig, ax = plt.subplots(figsize=(10, 6))
        bars = ax.barh(labels, values, color='#2ecc71')

        # Add value labels on bars
        for i, (bar, value) in enumerate(zip(bars, values)):
            ax.text(value + 0.5, i, str(int(value)), va='center', fontweight='bold')

        ax.set_xlabel('Numero Utenti', fontsize=12)
        ax.set_ylabel('Paese', fontsize=12)
        ax.set_title('Distribuzione Geografica Utenti', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3, axis='x')

        plt.tight_layout()
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()

        print(f"  ✓ {filename}")

    def plot_top_pages(self, filename: str):
        """Plot top pages as horizontal bar chart."""
        pages = self.summary['content']['pages']

        if not pages:
            print(f"⚠️  Nessun dato per le pagine")
            return

        # Get top 10
        items = list(pages.items())[:10]
        labels = [p[0][:40] + '...' if len(p[0]) > 40 else p[0] for p in items]
        values = [p[1] for p in items]

        fig, ax = plt.subplots(figsize=(12, 8))
        bars = ax.barh(range(len(labels)), values, color='#3498db')

        # Add value labels
        for i, (bar, value) in enumerate(zip(bars, values)):
            ax.text(value + 0.5, i, str(int(value)), va='center', fontweight='bold')

        ax.set_yticks(range(len(labels)))
        ax.set_yticklabels(labels, fontsize=9)
        ax.set_xlabel('Visualizzazioni', fontsize=12)
        ax.set_title('Top 10 Pagine Più Visualizzate', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3, axis='x')

        # Invert y-axis so top page is at top
        ax.invert_yaxis()

        plt.tight_layout()
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()

        print(f"  ✓ {filename}")

    def plot_user_trends(self, filename: str):
        """Plot 30/7/1 day user trends."""
        trends = self.data['user_trends']

        if not trends:
            print(f"⚠️  Nessun dato per user trends")
            return

        days = [t['day'] for t in trends]
        days_30 = [t['30_days'] for t in trends]
        days_7 = [t['7_days'] for t in trends]
        days_1 = [t['1_day'] for t in trends]

        # Convert to dates
        start_date = datetime.strptime(self.data['metadata']['start_date'], '%Y-%m-%d')
        dates = [start_date + timedelta(days=d) for d in days]

        fig, ax = plt.subplots(figsize=(12, 6))

        ax.plot(dates, days_30, label='30 giorni', linewidth=2, marker='o', markersize=4, color='#e74c3c')
        ax.plot(dates, days_7, label='7 giorni', linewidth=2, marker='s', markersize=4, color='#f39c12')
        ax.plot(dates, days_1, label='1 giorno', linewidth=2, marker='^', markersize=4, color='#3498db')

        ax.set_xlabel('Data', fontsize=12)
        ax.set_ylabel('Utenti Attivi', fontsize=12)
        ax.set_title('Trend Utenti Attivi (30/7/1 Giorni)', fontsize=14, fontweight='bold')
        ax.legend(loc='upper left', fontsize=10)
        ax.grid(True, alpha=0.3)

        # Format x-axis
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m'))
        plt.xticks(rotation=45)

        plt.tight_layout()
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()

        print(f"  ✓ {filename}")

    def plot_events(self, filename: str):
        """Plot events breakdown."""
        events = self.summary['content']['events']

        if not events:
            print(f"⚠️  Nessun dato per eventi")
            return

        # Sort by count
        sorted_events = sorted(events.items(), key=lambda x: x[1], reverse=True)
        labels = [e[0] for e in sorted_events]
        values = [e[1] for e in sorted_events]

        fig, ax = plt.subplots(figsize=(10, 6))
        bars = ax.bar(labels, values, color='#9b59b6')

        # Add value labels
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{int(height)}',
                   ha='center', va='bottom', fontweight='bold')

        ax.set_xlabel('Tipo Evento', fontsize=12)
        ax.set_ylabel('Conteggio', fontsize=12)
        ax.set_title('Distribuzione Eventi', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3, axis='y')

        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()

        print(f"  ✓ {filename}")


def main():
    """Main execution."""
    import os

    print("\n" + "=" * 80)
    print("VISUALIZZAZIONE DATI ANALYTICS - CasaDelleMagnolie.com")
    print("=" * 80 + "\n")

    # Load parsed data
    csv_file = "Istantanea_report.csv"
    summary_file = "analytics_summary.json"

    if not os.path.exists(csv_file):
        print(f"❌ File CSV non trovato: {csv_file}")
        print("Esegui prima analytics_analyzer.py")
        return

    # Parse data
    parser = GoogleAnalyticsParser(csv_file)
    data = parser.parse()

    # Load summary
    if os.path.exists(summary_file):
        with open(summary_file, 'r', encoding='utf-8') as f:
            summary = json.load(f)
    else:
        print(f"⚠️  Summary non trovato, rigenero...")
        from analytics_analyzer import AnalyticsAnalyzer
        analyzer = AnalyticsAnalyzer(data)
        summary = analyzer.generate_summary()

    # Create visualizations
    visualizer = AnalyticsVisualizer(data, summary)
    visualizer.create_all_charts("analytics")

    print("\n✅ Visualizzazioni completate!\n")


if __name__ == "__main__":
    main()
