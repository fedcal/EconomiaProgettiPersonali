#!/usr/bin/env python3
"""
Strategic Analysis for FedericoCalo.dev
Analyzes Google Analytics data and provides actionable recommendations
"""

import json
from datetime import datetime
from typing import Dict, List, Tuple


class StrategicAnalyzer:
    """Analyze data and provide strategic recommendations."""

    def __init__(self, summary: Dict):
        self.summary = summary
        self.recommendations = []
        self.insights = []
        self.warnings = []
        self.opportunities = []

    def analyze_all(self):
        """Run all analyses."""
        self._analyze_user_acquisition()
        self._analyze_traffic_sources()
        self._analyze_user_retention()
        self._analyze_content_performance()
        self._analyze_geography()
        self._analyze_engagement()
        self._analyze_growth_trend()

    def _analyze_user_acquisition(self):
        """Analyze user acquisition patterns."""
        users = self.summary['users']

        # All new users, no returning
        if users['returning_users'] == 0 and users['total_new_users'] > 0:
            self.warnings.append({
                'area': 'User Retention',
                'severity': 'ALTA',
                'issue': f'Zero utenti di ritorno su {users["total_new_users"]} totali',
                'impact': 'Mancanza di fidelizzazione utenti',
                'recommendation': [
                    'Implementa una newsletter per riportare gli utenti sul sito',
                    'Aggiungi contenuti freschi regolarmente (blog settimanale)',
                    'Crea una sezione "Progetti in corso" per incentivare visite ripetute',
                    'Considera notifiche push per nuovi articoli'
                ]
            })

        # Low average daily users
        if users['avg_daily_users'] < 5:
            self.insights.append({
                'area': 'Traffico',
                'type': 'Opportunità di crescita',
                'data': f'Media {users["avg_daily_users"]} utenti/giorno',
                'potential': 'Alto potenziale di crescita organica'
            })

    def _analyze_traffic_sources(self):
        """Analyze traffic source distribution."""
        sources = self.summary['traffic_sources']
        percentages = sources['source_percentages']

        # Analyze each source
        for source, percentage in percentages.items():
            if source == 'Organic Social' and percentage > 50:
                self.insights.append({
                    'area': 'Traffico Social',
                    'type': 'Punto di forza',
                    'data': f'{percentage}% da social media',
                    'action': 'Mantenere e potenziare presenza social'
                })

                self.recommendations.append({
                    'priority': 'MEDIA',
                    'category': 'Social Media',
                    'title': 'Ottimizza la strategia social',
                    'actions': [
                        'Identifica quale piattaforma social porta più traffico (LinkedIn, Twitter, etc.)',
                        'Pubblica contenuti regolarmente (2-3 volte/settimana)',
                        'Usa hashtag rilevanti per developer (#webdev, #javascript, etc.)',
                        'Condividi snippet di codice e tips dai tuoi articoli',
                        'Interagisci con community di sviluppatori'
                    ]
                })

            if source == 'Organic Search' and percentage < 10:
                self.warnings.append({
                    'area': 'SEO',
                    'severity': 'ALTA',
                    'issue': f'Solo {percentage}% di traffico da ricerca organica',
                    'impact': 'Scarsa visibilità su Google',
                    'recommendation': [
                        'Ottimizza meta tags (title, description) per ogni pagina',
                        'Aggiungi schema.org markup (Person, BlogPosting, Article)',
                        'Crea contenuti originali e di valore (tutorial, guide)',
                        'Migliora la velocità di caricamento del sito',
                        'Ottieni backlinks da siti autorevoli (guest posting)',
                        'Usa Google Search Console per identificare opportunità',
                        'Target keywords long-tail specifiche del tuo settore'
                    ]
                })

                self.recommendations.append({
                    'priority': 'ALTA',
                    'category': 'SEO',
                    'title': 'Piano SEO completo',
                    'actions': [
                        'Audit SEO completo con tools (Screaming Frog, Ahrefs)',
                        'Keyword research per il tuo settore',
                        'Ottimizza ogni articolo per 1-2 keywords specifiche',
                        'Crea pillar content (guide complete 2000+ parole)',
                        'Internal linking tra articoli correlati',
                        'Registra il sito su Google Search Console e Bing Webmaster',
                        'Submit sitemap.xml ai motori di ricerca'
                    ]
                })

            if source == 'Direct' and percentage > 30:
                self.insights.append({
                    'area': 'Traffico Diretto',
                    'type': 'Brand Awareness',
                    'data': f'{percentage}% di traffico diretto',
                    'meaning': 'Gli utenti conoscono già il tuo brand/URL'
                })

    def _analyze_user_retention(self):
        """Analyze user retention and return rate."""
        users = self.summary['users']

        return_rate = (users['returning_users'] / users['total_active_users'] * 100) if users['total_active_users'] > 0 else 0

        if return_rate < 10:
            self.recommendations.append({
                'priority': 'ALTA',
                'category': 'Retention',
                'title': 'Strategia di fidelizzazione utenti',
                'actions': [
                    'Newsletter mensile con updates e nuovi articoli',
                    'RSS feed per lettori abituali',
                    'Sezione "Aggiornamenti recenti" in homepage',
                    'Call-to-action per seguire sui social',
                    'Series di articoli collegati per incentivare ritorni',
                    'Email course gratuito su un topic specifico',
                    'Considera un mini-tool utile che richieda visite ripetute'
                ]
            })

    def _analyze_content_performance(self):
        """Analyze content and page performance."""
        content = self.summary['content']

        pages = content['pages']
        total_views = content['total_pageviews']
        unique_pages = content['unique_pages']

        # Calculate average views per page
        avg_views_per_page = total_views / unique_pages if unique_pages > 0 else 0

        if unique_pages > 0:
            # Identify top performing pages
            top_pages = list(pages.items())[:3]

            self.insights.append({
                'area': 'Content',
                'type': 'Top Performing Pages',
                'data': [{'page': p[0][:60], 'views': p[1]} for p in top_pages],
                'action': 'Analizza perché queste pagine performano meglio'
            })

            self.recommendations.append({
                'priority': 'MEDIA',
                'category': 'Content Strategy',
                'title': 'Ottimizza i contenuti top',
                'actions': [
                    f'Le tue top {len(top_pages)} pagine generano la maggior parte del traffico',
                    'Aggiungi CTA (Call-to-Action) nelle pagine più visitate',
                    'Link da pagine top a contenuti correlati',
                    'Aggiorna regolarmente i contenuti top con nuove informazioni',
                    'Espandi i topic delle pagine di successo con nuovi articoli',
                    'Aggiungi share buttons social nelle pagine più viste'
                ]
            })

        # Low page diversity
        if unique_pages < 10:
            self.recommendations.append({
                'priority': 'ALTA',
                'category': 'Content Creation',
                'title': 'Espandi il contenuto del sito',
                'actions': [
                    f'Hai solo {unique_pages} pagine indicizzate - crea più contenuto!',
                    'Pubblica almeno 1-2 articoli tecnici al mese',
                    'Crea tutorial step-by-step sui tuoi progetti',
                    'Documenta le sfide tecniche che hai risolto',
                    'Case studies dei tuoi progetti principali',
                    'Guide "How-to" su tecnologie che usi',
                    'Considera una sezione FAQ o Resources'
                ]
            })

        # Blog analysis
        blog_pages = [p for p in pages.keys() if 'blog' in p.lower() or 'articol' in p.lower()]
        if blog_pages:
            blog_views = sum(pages[p] for p in blog_pages)
            blog_percentage = (blog_views / total_views * 100) if total_views > 0 else 0

            if blog_percentage > 15:
                self.insights.append({
                    'area': 'Blog',
                    'type': 'Punto di forza',
                    'data': f'{blog_percentage:.1f}% del traffico va al blog',
                    'action': 'Il blog funziona - continua a pubblicare!'
                })

    def _analyze_geography(self):
        """Analyze geographic distribution."""
        geo = self.summary['geography']

        countries = geo['countries']
        total = geo['total_users']

        # Top country concentration
        top_country = geo['top_country']
        top_percentage = geo['country_percentages'].get(top_country, 0)

        if top_percentage > 40:
            self.insights.append({
                'area': 'Geografia',
                'type': 'Concentrazione geografica',
                'data': f'{top_percentage}% utenti da {top_country}',
                'implication': 'Mercato principale identificato'
            })

            if top_country == 'US':
                self.recommendations.append({
                    'priority': 'BASSA',
                    'category': 'Internazionalizzazione',
                    'title': 'Ottimizza per mercato USA',
                    'actions': [
                        'Considera contenuti in inglese (se non già presente)',
                        'Orari di pubblicazione allineati con timezone USA',
                        'Esempi e case studies rilevanti per mercato US',
                        'Partecipa a community tech USA (Dev.to, Hashnode, Reddit)',
                        'Networking su LinkedIn con professionisti USA'
                    ]
                })

            if top_country == 'IT':
                self.recommendations.append({
                    'priority': 'MEDIA',
                    'category': 'Mercato Locale',
                    'title': 'Rafforza presenza in Italia',
                    'actions': [
                        'Partecipa a community italiane (devs.it, forum)',
                        'Collabora con tech blog italiani',
                        'Considera eventi/meetup locali',
                        'Network con aziende tech italiane',
                        'Guest posting su blog IT del settore'
                    ]
                })

        # International diversity
        country_count = geo['country_count']
        if country_count > 5:
            self.insights.append({
                'area': 'Reach Internazionale',
                'type': 'Diversificazione',
                'data': f'Utenti da {country_count} paesi',
                'meaning': 'Buona visibilità internazionale'
            })

    def _analyze_engagement(self):
        """Analyze user engagement metrics."""
        engagement = self.summary['engagement']

        avg_time = engagement['avg_engagement_minutes']

        # Low engagement time
        if avg_time < 1:
            self.warnings.append({
                'area': 'Engagement',
                'severity': 'MEDIA',
                'issue': f'Tempo medio di coinvolgimento: {avg_time:.2f} minuti',
                'impact': 'Gli utenti abbandonano rapidamente',
                'recommendation': [
                    'Migliora la leggibilità: paragrafi brevi, liste puntate',
                    'Aggiungi elementi visivi: immagini, code snippets, diagrammi',
                    'Inserisci video o demo interattive',
                    'Hook iniziali più coinvolgenti (intro accattivante)',
                    'Suddividi contenuti lunghi in sezioni con sottotitoli',
                    'Aggiungi table of contents per articoli lunghi',
                    'Riduci distrazioni e elementi non necessari'
                ]
            })

            self.recommendations.append({
                'priority': 'ALTA',
                'category': 'User Experience',
                'title': 'Migliora l\'engagement degli utenti',
                'actions': [
                    'Audit UX completo del sito',
                    'Verifica velocità caricamento (target < 3 secondi)',
                    'Ottimizza per mobile (responsive design)',
                    'Aggiungi elementi interattivi (code playground, demo)',
                    'Migliora la navigazione (menu chiaro, breadcrumbs)',
                    'Related articles a fine pagina',
                    'Evita popup invasivi che disturbano la lettura'
                ]
            })

    def _analyze_growth_trend(self):
        """Analyze growth trends."""
        users = self.summary['users']
        trend = users['growth_trend']

        if trend == 'crescita':
            self.insights.append({
                'area': 'Crescita',
                'type': 'Trend positivo',
                'data': 'Trend in crescita nel periodo analizzato',
                'action': 'Identifica cosa ha funzionato e replica il successo'
            })

            self.recommendations.append({
                'priority': 'ALTA',
                'category': 'Growth Hacking',
                'title': 'Mantieni e accelera la crescita',
                'actions': [
                    'Identifica i canali che hanno portato più traffico',
                    'Analizza quali contenuti hanno performato meglio',
                    'Raddoppia gli sforzi sui canali di successo',
                    'Pubblica con maggiore frequenza',
                    'Cross-posting su piattaforme multiple (Dev.to, Medium, Hashnode)',
                    'Collaborazioni con altri developer/blogger',
                    'Partecipa attivamente a discussion su social/forum'
                ]
            })

        elif trend == 'decrescita':
            self.warnings.append({
                'area': 'Crescita',
                'severity': 'ALTA',
                'issue': 'Trend in decrescita',
                'impact': 'Perdita di traffico e visibilità',
                'recommendation': [
                    'Analizza cosa è cambiato nel periodo',
                    'Verifica se ci sono problemi tecnici (downtime, errori)',
                    'Controlla penalizzazioni SEO',
                    'Rivedi la strategia di content marketing',
                    'Incrementa frequenza pubblicazioni',
                    'Riattiva canali social dormienti'
                ]
            })

    def generate_priority_matrix(self) -> Dict:
        """Generate priority matrix for recommendations."""
        high_priority = [r for r in self.recommendations if r['priority'] == 'ALTA']
        medium_priority = [r for r in self.recommendations if r['priority'] == 'MEDIA']
        low_priority = [r for r in self.recommendations if r['priority'] == 'BASSA']

        return {
            'immediate_action': high_priority[:3],  # Top 3 high priority
            'short_term': medium_priority,
            'long_term': low_priority
        }

    def generate_action_plan(self) -> str:
        """Generate detailed action plan."""
        plan = []

        plan.append("=" * 80)
        plan.append("PIANO D'AZIONE STRATEGICO - FEDERICOCALO.DEV")
        plan.append("=" * 80)
        plan.append("")

        # Executive Summary
        plan.append("EXECUTIVE SUMMARY")
        plan.append("-" * 80)
        plan.append(f"Analisi del periodo: {self.summary['period']['start']} - {self.summary['period']['end']}")
        plan.append(f"Utenti totali: {self.summary['users']['total_active_users']}")
        plan.append(f"Trend: {self.summary['users']['growth_trend'].upper()}")
        plan.append(f"Problemi critici identificati: {len(self.warnings)}")
        plan.append(f"Opportunità di crescita: {len(self.opportunities)}")
        plan.append("")

        # Critical Warnings
        if self.warnings:
            plan.append("⚠️  PROBLEMI CRITICI DA RISOLVERE")
            plan.append("-" * 80)
            for idx, warning in enumerate(self.warnings, 1):
                plan.append(f"\n{idx}. {warning['area']} - {warning['issue']}")
                plan.append(f"   Severità: {warning['severity']}")
                plan.append(f"   Impatto: {warning['impact']}")
                plan.append(f"   Raccomandazioni:")
                for rec in warning['recommendation']:
                    plan.append(f"   • {rec}")
            plan.append("")

        # Key Insights
        if self.insights:
            plan.append("💡 INSIGHTS CHIAVE")
            plan.append("-" * 80)
            for idx, insight in enumerate(self.insights, 1):
                plan.append(f"\n{idx}. {insight['area']} - {insight['type']}")
                if isinstance(insight['data'], str):
                    plan.append(f"   {insight['data']}")
                if 'action' in insight:
                    plan.append(f"   → {insight['action']}")
            plan.append("")

        # Priority Matrix
        matrix = self.generate_priority_matrix()

        plan.append("🎯 AZIONI PRIORITARIE")
        plan.append("-" * 80)

        if matrix['immediate_action']:
            plan.append("\n📌 AZIONE IMMEDIATA (Prossime 2 settimane):")
            for idx, rec in enumerate(matrix['immediate_action'], 1):
                plan.append(f"\n{idx}. {rec['category']}: {rec['title']}")
                for action in rec['actions'][:3]:  # Top 3 actions
                    plan.append(f"   ✓ {action}")

        if matrix['short_term']:
            plan.append("\n📅 BREVE TERMINE (Prossimo mese):")
            for idx, rec in enumerate(matrix['short_term'], 1):
                plan.append(f"\n{idx}. {rec['category']}: {rec['title']}")
                for action in rec['actions'][:2]:  # Top 2 actions
                    plan.append(f"   ✓ {action}")

        if matrix['long_term']:
            plan.append("\n🔮 LUNGO TERMINE (Prossimi 3-6 mesi):")
            for idx, rec in enumerate(matrix['long_term'], 1):
                plan.append(f"{idx}. {rec['title']}")

        plan.append("")
        plan.append("=" * 80)

        # Quick Wins
        plan.append("\n⚡ QUICK WINS (Implementabili in 1 giorno)")
        plan.append("-" * 80)
        quick_wins = [
            "Aggiungi meta description su tutte le pagine",
            "Registra il sito su Google Search Console",
            "Aggiungi sitemap.xml",
            "Ottimizza title tags per SEO",
            "Aggiungi schema.org Person markup",
            "Crea profilo LinkedIn completo con link al sito",
            "Pubblica 1 post social con link a miglior articolo",
            "Aggiungi Google Analytics events per tracking CTA",
            "Verifica e correggi broken links",
            "Ottimizza immagini per web (compressione)"
        ]
        for win in quick_wins:
            plan.append(f"  ✓ {win}")

        plan.append("")
        plan.append("=" * 80)

        return "\n".join(plan)


def main():
    """Main execution."""
    import os

    print("\n" + "=" * 80)
    print("ANALISI STRATEGICA - FEDERICOCALO.DEV")
    print("=" * 80 + "\n")

    # Load summary
    summary_file = "analytics_summary.json"

    if not os.path.exists(summary_file):
        print(f"❌ File summary non trovato: {summary_file}")
        print("Esegui prima analytics_analyzer.py")
        return

    with open(summary_file, 'r', encoding='utf-8') as f:
        summary = json.load(f)

    # Run strategic analysis
    analyzer = StrategicAnalyzer(summary)
    analyzer.analyze_all()

    # Generate action plan
    action_plan = analyzer.generate_action_plan()

    print(action_plan)

    # Save to file
    output_file = "strategic_action_plan.txt"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(action_plan)

    print(f"\n💾 Piano d'azione salvato in: {output_file}\n")

    # Save detailed JSON
    detailed_output = {
        'generated_at': datetime.now().isoformat(),
        'warnings': analyzer.warnings,
        'insights': analyzer.insights,
        'recommendations': analyzer.recommendations,
        'priority_matrix': analyzer.generate_priority_matrix()
    }

    json_file = "strategic_recommendations.json"
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(detailed_output, f, ensure_ascii=False, indent=2)

    print(f"💾 Raccomandazioni dettagliate salvate in: {json_file}\n")


if __name__ == "__main__":
    main()
