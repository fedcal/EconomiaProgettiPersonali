"""
Report Generator - Generatore di report in diversi formati
"""

import json
import os
from datetime import datetime
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)


class ReportGenerator:
    """Generatore di report"""
    
    def __init__(self, report_format: str = 'html'):
        """
        Inizializza il generatore
        
        Args:
            report_format: Formato report (html, pdf, markdown, json)
        """
        self.format = report_format
    
    def generate(self, source_name: str, analysis_data: Dict, config: Dict) -> str:
        """
        Genera il report
        
        Args:
            source_name: Nome della fonte
            analysis_data: Dati analizzati
            config: Configurazione
        
        Returns:
            Percorso al report generato
        """
        if self.format == 'html':
            return self._generate_html(source_name, analysis_data, config)
        elif self.format == 'markdown':
            return self._generate_markdown(source_name, analysis_data, config)
        elif self.format == 'json':
            return self._generate_json(source_name, analysis_data, config)
        else:
            return self._generate_text(source_name, analysis_data, config)
    
    def _generate_html(self, source_name: str, analysis_data: Dict, config: Dict) -> str:
        """Genera report HTML"""
        output_dir = config.get('output_dir', './reports')
        os.makedirs(output_dir, exist_ok=True)
        
        filename = f"{source_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        filepath = os.path.join(output_dir, filename)
        
        html_content = f"""
<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Web Analytics Report - {source_name}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }}
        .container {{ max-width: 1200px; margin: 0 auto; background-color: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        h1 {{ color: #333; border-bottom: 3px solid #007bff; padding-bottom: 10px; }}
        h2 {{ color: #555; margin-top: 30px; }}
        .metric {{ display: inline-block; margin: 10px 20px 10px 0; padding: 15px; background-color: #f9f9f9; border-left: 4px solid #007bff; border-radius: 4px; min-width: 200px; }}
        .metric-value {{ font-size: 24px; font-weight: bold; color: #007bff; }}
        .metric-label {{ font-size: 12px; color: #666; margin-top: 5px; }}
        table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
        th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }}
        th {{ background-color: #f9f9f9; font-weight: bold; }}
        tr:hover {{ background-color: #f5f5f5; }}
        .footer {{ margin-top: 40px; padding-top: 20px; border-top: 1px solid #ddd; color: #666; font-size: 12px; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>📊 Web Analytics Report</h1>
        <p><strong>Fonte:</strong> {source_name}</p>
        <p><strong>Generato:</strong> {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}</p>
        
        <h2>📈 Metriche Principali</h2>
"""
        
        # Aggiungi metriche principali
        analysis = analysis_data.get('analysis', {})
        traffic = analysis.get('traffic', {})
        users = analysis.get('users', {})
        conversions = analysis.get('conversions', {})
        engagement = analysis.get('engagement', {})
        
        metrics = [
            ('Total Sessions', traffic.get('total_sessions', 0)),
            ('Unique Visitors', users.get('total_users', 0)),
            ('Conversion Rate', f"{conversions.get('conversion_rate', 0):.2f}%"),
            ('Avg Session Duration', f"{engagement.get('avg_time_on_site', 0):.0f}s"),
            ('Bounce Rate', f"{traffic.get('bounce_rate', 0):.2f}%"),
            ('Pages per Session', f"{traffic.get('pages_per_session', 0):.1f}"),
        ]
        
        for label, value in metrics:
            html_content += f"""
        <div class="metric">
            <div class="metric-value">{value}</div>
            <div class="metric-label">{label}</div>
        </div>
"""
        
        # Aggiungi sezioni dettagliate
        html_content += """
        <h2>🔍 Analisi Dettagliata</h2>
"""
        
        if traffic.get('top_pages'):
            html_content += "<h3>Top Pages</h3><table><tr><th>Page</th><th>Views</th></tr>"
            for page, count in list(traffic['top_pages'].items())[:10]:
                html_content += f"<tr><td>{page}</td><td>{count}</td></tr>"
            html_content += "</table>"
        
        if traffic.get('traffic_sources'):
            html_content += "<h3>Traffic Sources</h3><table><tr><th>Source</th><th>Sessions</th></tr>"
            for source, count in list(traffic['traffic_sources'].items())[:10]:
                html_content += f"<tr><td>{source}</td><td>{count}</td></tr>"
            html_content += "</table>"
        
        html_content += """
        <div class="footer">
            <p>Report generato automaticamente dal Web Analytics Agent</p>
            <p>© 2026 PlayTheEvent Analytics System</p>
        </div>
    </div>
</body>
</html>
"""
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        logger.info(f"✅ HTML report generato: {filepath}")
        return filepath
    
    def _generate_markdown(self, source_name: str, analysis_data: Dict, config: Dict) -> str:
        """Genera report Markdown"""
        output_dir = config.get('output_dir', './reports')
        os.makedirs(output_dir, exist_ok=True)
        
        filename = f"{source_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        filepath = os.path.join(output_dir, filename)
        
        analysis = analysis_data.get('analysis', {})
        traffic = analysis.get('traffic', {})
        users = analysis.get('users', {})
        conversions = analysis.get('conversions', {})
        engagement = analysis.get('engagement', {})
        
        md_content = f"""# 📊 Web Analytics Report

**Source:** {source_name}  
**Generated:** {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}

## 📈 Key Metrics

| Metric | Value |
|--------|-------|
| Total Sessions | {traffic.get('total_sessions', 0)} |
| Unique Visitors | {users.get('total_users', 0)} |
| Conversion Rate | {conversions.get('conversion_rate', 0):.2f}% |
| Avg Session Duration | {engagement.get('avg_time_on_site', 0):.0f}s |
| Bounce Rate | {traffic.get('bounce_rate', 0):.2f}% |
| Pages per Session | {traffic.get('pages_per_session', 0):.1f} |

## 🔍 Traffic Analysis

### Top Pages
"""
        
        if traffic.get('top_pages'):
            for page, count in list(traffic['top_pages'].items())[:10]:
                md_content += f"- **{page}**: {count} views\n"
        
        md_content += f"""

### Traffic Sources
"""
        
        if traffic.get('traffic_sources'):
            for source, count in list(traffic['traffic_sources'].items())[:10]:
                md_content += f"- **{source}**: {count} sessions\n"
        
        md_content += """

## 👥 User Analysis

"""
        
        if users.get('user_segments'):
            md_content += "### User Segments\n"
            for segment, count in users['user_segments'].items():
                md_content += f"- **{segment}**: {count}\n"
        
        md_content += f"""

## 💰 Conversion Analysis

- **Total Conversions**: {conversions.get('total_conversions', 0)}
- **Conversion Rate**: {conversions.get('conversion_rate', 0):.2f}%
- **Total Conversion Value**: ${conversions.get('conversion_value', 0):.2f}
- **Avg Conversion Value**: ${conversions.get('avg_conversion_value', 0):.2f}

---

*Report generato automaticamente dal Web Analytics Agent*
"""
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(md_content)
        
        logger.info(f"✅ Markdown report generato: {filepath}")
        return filepath
    
    def _generate_json(self, source_name: str, analysis_data: Dict, config: Dict) -> str:
        """Genera report JSON"""
        output_dir = config.get('output_dir', './reports')
        os.makedirs(output_dir, exist_ok=True)
        
        filename = f"{source_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        filepath = os.path.join(output_dir, filename)
        
        report_data = {
            'source': source_name,
            'generated_at': datetime.now().isoformat(),
            'analysis': analysis_data.get('analysis', {})
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=2, default=str)
        
        logger.info(f"✅ JSON report generato: {filepath}")
        return filepath
    
    def _generate_text(self, source_name: str, analysis_data: Dict, config: Dict) -> str:
        """Genera report testo"""
        output_dir = config.get('output_dir', './reports')
        os.makedirs(output_dir, exist_ok=True)
        
        filename = f"{source_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        filepath = os.path.join(output_dir, filename)
        
        analysis = analysis_data.get('analysis', {})
        traffic = analysis.get('traffic', {})
        users = analysis.get('users', {})
        
        text_content = f"""
WEB ANALYTICS REPORT
{'='*70}

Source: {source_name}
Generated: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}

KEY METRICS
-----------
Total Sessions: {traffic.get('total_sessions', 0)}
Unique Visitors: {users.get('total_users', 0)}
Bounce Rate: {traffic.get('bounce_rate', 0):.2f}%
Avg Session Duration: {traffic.get('avg_session_duration', 0):.0f}s
Pages per Session: {traffic.get('pages_per_session', 0):.1f}

{'='*70}
"""
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(text_content)
        
        logger.info(f"✅ Text report generato: {filepath}")
        return filepath
