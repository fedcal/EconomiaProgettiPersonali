#!/usr/bin/env python3
"""
Google Analytics CSV Analyzer for FedericoCalo Portfolio
Analyzes exported Google Analytics data and generates detailed reports
"""

import csv
import re
from datetime import datetime, timedelta
from collections import defaultdict
import json
from typing import Dict, List, Tuple


class GoogleAnalyticsParser:
    """Parser for Google Analytics CSV exports."""

    def __init__(self, csv_file: str):
        self.csv_file = csv_file
        self.data = {
            'metadata': {},
            'daily_active_users': [],
            'daily_new_users': [],
            'engagement_duration': [],
            'revenue': [],
            'traffic_sources_new': {},
            'traffic_sources_session': {},
            'geography': {},
            'user_trends': [],
            'retention': [],
            'pages': {},
            'events': {}
        }

    def parse(self):
        """Parse the entire CSV file."""
        with open(self.csv_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Extract metadata
        self._extract_metadata(content)

        # Split content into sections
        sections = content.split('\n\n')

        for section in sections:
            if 'Utenti attivi' in section and 'N° giorno' in section:
                self._parse_daily_data(section, 'daily_active_users')
            elif 'Nuovi utenti' in section and 'N° giorno' in section:
                self._parse_daily_data(section, 'daily_new_users')
            elif 'Durata media del coinvolgimento' in section:
                self._parse_daily_data(section, 'engagement_duration')
            elif 'Entrate totali' in section:
                self._parse_daily_data(section, 'revenue')
            elif 'Da dove provengono i nuovi utenti?' in section:
                self._parse_traffic_sources(section, 'traffic_sources_new')
            elif 'Gruppo di canali principale della sessione' in section:
                self._parse_traffic_sources(section, 'traffic_sources_session')
            elif 'ID Paese' in section or ('Paese' in section and 'Utenti attivi' in section):
                self._parse_geography(section)
            elif 'tendenza degli utenti attivi' in section:
                self._parse_user_trends(section)
            elif 'Titolo pagina' in section:
                self._parse_pages(section)
            elif 'Nome evento' in section and 'Conteggio eventi' in section:
                self._parse_events(section)

        return self.data

    def _extract_metadata(self, content: str):
        """Extract metadata from CSV header."""
        account_match = re.search(r'Account:\s*(.+)', content)
        property_match = re.search(r'Proprietà:\s*(.+)', content)
        start_date_match = re.search(r'Data di inizio:\s*(\d{8})', content)
        end_date_match = re.search(r'Data di fine:\s*(\d{8})', content)

        if account_match:
            self.data['metadata']['account'] = account_match.group(1).strip()
        if property_match:
            self.data['metadata']['property'] = property_match.group(1).strip()
        if start_date_match:
            date_str = start_date_match.group(1)
            self.data['metadata']['start_date'] = datetime.strptime(date_str, '%Y%m%d').strftime('%Y-%m-%d')
        if end_date_match:
            date_str = end_date_match.group(1)
            self.data['metadata']['end_date'] = datetime.strptime(date_str, '%Y%m%d').strftime('%Y-%m-%d')

    def _parse_daily_data(self, section: str, key: str):
        """Parse daily numerical data."""
        lines = section.strip().split('\n')
        data = []

        for line in lines:
            if line.startswith('#') or 'N° giorno' in line or 'Data di' in line:
                continue

            parts = line.split(',')
            if len(parts) == 2:
                try:
                    day_num = int(parts[0])
                    value = float(parts[1])
                    data.append({'day': day_num, 'value': value})
                except ValueError:
                    continue

        self.data[key] = data

    def _parse_traffic_sources(self, section: str, key: str):
        """Parse traffic source data."""
        lines = section.strip().split('\n')
        sources = {}

        for line in lines:
            if line.startswith('#') or 'Gruppo di canali' in line or 'Data di' in line:
                continue

            parts = line.split(',')
            if len(parts) == 2:
                try:
                    source = parts[0].strip()
                    count = int(parts[1])
                    if source:
                        sources[source] = count
                except ValueError:
                    continue

        self.data[key] = sources

    def _parse_geography(self, section: str):
        """Parse geography data."""
        lines = section.strip().split('\n')
        countries = {}

        for line in lines:
            if line.startswith('#') or 'Paese' in line or 'Data di' in line or 'ID Paese' in line:
                continue

            parts = line.split(',')
            if len(parts) == 2:
                try:
                    country = parts[0].strip()
                    count = int(parts[1])
                    if country and len(country) <= 3:  # Country codes or short names
                        countries[country] = count
                except ValueError:
                    continue

        if countries:
            self.data['geography'] = countries

    def _parse_user_trends(self, section: str):
        """Parse user trend data (30/7/1 day active users)."""
        lines = section.strip().split('\n')
        trends = []

        for line in lines:
            if line.startswith('#') or 'N° giorno' in line or 'Data di' in line:
                continue

            parts = line.split(',')
            if len(parts) == 4:
                try:
                    day = int(parts[0])
                    days_30 = int(parts[1])
                    days_7 = int(parts[2])
                    days_1 = int(parts[3])
                    trends.append({
                        'day': day,
                        '30_days': days_30,
                        '7_days': days_7,
                        '1_day': days_1
                    })
                except ValueError:
                    continue

        self.data['user_trends'] = trends

    def _parse_pages(self, section: str):
        """Parse page views data."""
        lines = section.strip().split('\n')
        pages = {}

        for line in lines:
            if line.startswith('#') or 'Titolo pagina' in line or 'Data di' in line:
                continue

            # Handle titles with commas (quoted)
            if line.startswith('"'):
                match = re.match(r'"([^"]+)",(\d+)', line)
                if match:
                    title = match.group(1)
                    views = int(match.group(2))
                    pages[title] = views
            else:
                parts = line.rsplit(',', 1)
                if len(parts) == 2:
                    try:
                        title = parts[0].strip()
                        views = int(parts[1])
                        if title:
                            pages[title] = views
                    except ValueError:
                        continue

        self.data['pages'] = pages

    def _parse_events(self, section: str):
        """Parse events data."""
        lines = section.strip().split('\n')
        events = {}

        for line in lines:
            if line.startswith('#') or 'Nome evento' in line or 'Data di' in line:
                continue

            parts = line.split(',')
            if len(parts) == 2:
                try:
                    event_name = parts[0].strip()
                    count = int(parts[1])
                    if event_name:
                        events[event_name] = count
                except ValueError:
                    continue

        self.data['events'] = events


class AnalyticsAnalyzer:
    """Analyzer for Google Analytics data."""

    def __init__(self, data: Dict):
        self.data = data

    def generate_summary(self) -> Dict:
        """Generate summary statistics."""
        summary = {
            'period': {
                'start': self.data['metadata'].get('start_date', 'N/A'),
                'end': self.data['metadata'].get('end_date', 'N/A'),
                'duration_days': len(self.data['daily_active_users'])
            },
            'users': self._analyze_users(),
            'traffic_sources': self._analyze_traffic(),
            'geography': self._analyze_geography(),
            'content': self._analyze_content(),
            'engagement': self._analyze_engagement()
        }

        return summary

    def _analyze_users(self) -> Dict:
        """Analyze user statistics."""
        active_users = [d['value'] for d in self.data['daily_active_users']]
        new_users = [d['value'] for d in self.data['daily_new_users']]

        total_active = sum(active_users)
        total_new = sum(new_users)
        returning_users = total_active - total_new

        # Find peak day
        peak_day_data = max(self.data['daily_active_users'], key=lambda x: x['value'], default={'day': 0, 'value': 0})

        return {
            'total_active_users': int(total_active),
            'total_new_users': int(total_new),
            'returning_users': int(returning_users),
            'avg_daily_users': round(total_active / len(active_users) if active_users else 0, 2),
            'peak_day': peak_day_data['day'],
            'peak_day_users': int(peak_day_data['value']),
            'growth_trend': self._calculate_growth_trend(active_users)
        }

    def _calculate_growth_trend(self, values: List[float]) -> str:
        """Calculate growth trend."""
        if len(values) < 2:
            return "insufficient_data"

        # Compare first half vs second half
        mid = len(values) // 2
        first_half_avg = sum(values[:mid]) / mid if mid > 0 else 0
        second_half_avg = sum(values[mid:]) / (len(values) - mid) if len(values) - mid > 0 else 0

        if second_half_avg > first_half_avg * 1.1:
            return "crescita"
        elif second_half_avg < first_half_avg * 0.9:
            return "decrescita"
        else:
            return "stabile"

    def _analyze_traffic(self) -> Dict:
        """Analyze traffic sources."""
        sources_new = self.data['traffic_sources_new']
        sources_session = self.data['traffic_sources_session']

        total_new = sum(sources_new.values()) if sources_new else 0
        total_sessions = sum(sources_session.values()) if sources_session else 0

        return {
            'new_users_by_source': sources_new,
            'sessions_by_source': sources_session,
            'total_new_users': total_new,
            'total_sessions': total_sessions,
            'top_source': max(sources_new.items(), key=lambda x: x[1])[0] if sources_new else 'N/A',
            'source_percentages': {
                source: round((count / total_new * 100), 2) if total_new > 0 else 0
                for source, count in sources_new.items()
            }
        }

    def _analyze_geography(self) -> Dict:
        """Analyze geographic distribution."""
        geo = self.data['geography']
        total = sum(geo.values()) if geo else 0

        sorted_countries = sorted(geo.items(), key=lambda x: x[1], reverse=True)

        return {
            'countries': geo,
            'total_users': total,
            'top_country': sorted_countries[0][0] if sorted_countries else 'N/A',
            'top_country_users': sorted_countries[0][1] if sorted_countries else 0,
            'country_count': len(geo),
            'country_percentages': {
                country: round((count / total * 100), 2) if total > 0 else 0
                for country, count in geo.items()
            }
        }

    def _analyze_content(self) -> Dict:
        """Analyze content performance."""
        pages = self.data['pages']
        events = self.data['events']

        total_pageviews = sum(pages.values()) if pages else 0
        total_events = sum(events.values()) if events else 0

        sorted_pages = sorted(pages.items(), key=lambda x: x[1], reverse=True)

        return {
            'total_pageviews': total_pageviews,
            'unique_pages': len(pages),
            'top_page': sorted_pages[0][0] if sorted_pages else 'N/A',
            'top_page_views': sorted_pages[0][1] if sorted_pages else 0,
            'pages': dict(sorted_pages[:10]),  # Top 10 pages
            'events': events,
            'total_events': total_events
        }

    def _analyze_engagement(self) -> Dict:
        """Analyze user engagement."""
        engagement_data = self.data['engagement_duration']

        if not engagement_data:
            return {
                'avg_engagement_seconds': 0,
                'total_engagement_time': 0
            }

        valid_engagements = [d['value'] for d in engagement_data if d['value'] > 0]

        avg_engagement = sum(valid_engagements) / len(valid_engagements) if valid_engagements else 0

        return {
            'avg_engagement_seconds': round(avg_engagement, 2),
            'avg_engagement_minutes': round(avg_engagement / 60, 2),
            'engaged_days': len(valid_engagements)
        }

    def generate_report(self) -> str:
        """Generate a text report."""
        summary = self.generate_summary()

        report = []
        report.append("=" * 80)
        report.append("REPORT ANALYTICS - FEDERICOCALO.DEV")
        report.append("=" * 80)
        report.append("")

        # Period
        report.append(f"Periodo analizzato: {summary['period']['start']} - {summary['period']['end']}")
        report.append(f"Durata: {summary['period']['duration_days']} giorni")
        report.append("")

        # Users
        report.append("UTENTI")
        report.append("-" * 80)
        report.append(f"Utenti attivi totali: {summary['users']['total_active_users']}")
        report.append(f"Nuovi utenti: {summary['users']['total_new_users']}")
        report.append(f"Utenti di ritorno: {summary['users']['returning_users']}")
        report.append(f"Media utenti giornalieri: {summary['users']['avg_daily_users']}")
        report.append(f"Picco utenti: {summary['users']['peak_day_users']} (giorno {summary['users']['peak_day']})")
        report.append(f"Trend: {summary['users']['growth_trend']}")
        report.append("")

        # Traffic Sources
        report.append("SORGENTI TRAFFICO")
        report.append("-" * 80)
        for source, percentage in summary['traffic_sources']['source_percentages'].items():
            count = summary['traffic_sources']['new_users_by_source'][source]
            report.append(f"{source}: {count} utenti ({percentage}%)")
        report.append(f"Sorgente principale: {summary['traffic_sources']['top_source']}")
        report.append("")

        # Geography
        report.append("DISTRIBUZIONE GEOGRAFICA")
        report.append("-" * 80)
        report.append(f"Paesi raggiunti: {summary['geography']['country_count']}")
        report.append(f"Paese principale: {summary['geography']['top_country']} ({summary['geography']['top_country_users']} utenti)")
        report.append("")
        report.append("Top 5 paesi:")
        sorted_countries = sorted(
            summary['geography']['country_percentages'].items(),
            key=lambda x: x[1],
            reverse=True
        )[:5]
        for country, percentage in sorted_countries:
            count = summary['geography']['countries'][country]
            report.append(f"  {country}: {count} utenti ({percentage}%)")
        report.append("")

        # Content
        report.append("CONTENUTI")
        report.append("-" * 80)
        report.append(f"Visualizzazioni totali: {summary['content']['total_pageviews']}")
        report.append(f"Pagine uniche: {summary['content']['unique_pages']}")
        report.append(f"Eventi totali: {summary['content']['total_events']}")
        report.append("")
        report.append("Top 5 pagine:")
        for idx, (page, views) in enumerate(list(summary['content']['pages'].items())[:5], 1):
            # Truncate long titles
            short_title = page[:70] + "..." if len(page) > 70 else page
            report.append(f"  {idx}. {short_title} ({views} views)")
        report.append("")

        # Engagement
        report.append("COINVOLGIMENTO")
        report.append("-" * 80)
        report.append(f"Tempo medio di coinvolgimento: {summary['engagement']['avg_engagement_minutes']} minuti")
        report.append(f"Giorni con utenti coinvolti: {summary['engagement']['engaged_days']}")
        report.append("")

        report.append("=" * 80)

        return "\n".join(report)


def main():
    """Main execution function."""
    import os

    print("\n" + "=" * 80)
    print("GOOGLE ANALYTICS ANALYZER - FedericoCalo.dev")
    print("=" * 80 + "\n")

    # Find CSV file
    csv_file = "Istantanea_report.csv"

    if not os.path.exists(csv_file):
        print(f"❌ File CSV non trovato: {csv_file}")
        print("Assicurati di essere nella directory corretta.")
        return

    print(f"📊 Analisi del file: {csv_file}\n")

    # Parse CSV
    parser = GoogleAnalyticsParser(csv_file)
    data = parser.parse()

    print(f"✅ Dati parsati con successo!")
    print(f"   Periodo: {data['metadata'].get('start_date', 'N/A')} - {data['metadata'].get('end_date', 'N/A')}\n")

    # Analyze data
    analyzer = AnalyticsAnalyzer(data)
    summary = analyzer.generate_summary()

    # Generate text report
    report = analyzer.generate_report()
    print(report)

    # Save JSON summary
    json_output = "analytics_summary.json"
    with open(json_output, 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)

    print(f"\n💾 Summary salvato in: {json_output}")

    # Save text report
    txt_output = "analytics_report.txt"
    with open(txt_output, 'w', encoding='utf-8') as f:
        f.write(report)

    print(f"💾 Report salvato in: {txt_output}\n")


if __name__ == "__main__":
    main()
