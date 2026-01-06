#!/usr/bin/env python3
"""
Strategic Analysis for CasaDelleMagnolie.com (Vacation Rental)
Analyzes Google Analytics data and provides actionable recommendations for vacation rental business
"""

import json
from datetime import datetime
from typing import Dict, List


class VacationRentalAnalyzer:
    """Strategic analyzer specifically for vacation rental websites."""

    def __init__(self, summary: Dict):
        self.summary = summary
        self.recommendations = []
        self.insights = []
        self.warnings = []
        self.opportunities = []

    def analyze_all(self):
        """Run all analyses specific to vacation rental business."""
        self._analyze_conversion_funnel()
        self._analyze_traffic_sources()
        self._analyze_local_seo()
        self._analyze_content_completeness()
        self._analyze_geography_targeting()
        self._analyze_engagement()
        self._analyze_seasonality()
        self._analyze_competition()

    def _analyze_conversion_funnel(self):
        """Analyze booking conversion funnel."""
        content = self.summary['content']
        pages = content['pages']

        # Single page suggests limited content
        if content['unique_pages'] <= 1:
            self.warnings.append({
                'area': 'Content & Conversion',
                'severity': 'CRITICA',
                'issue': 'Sito con una sola pagina visitata',
                'impact': 'Impossibile guidare l\'utente verso la prenotazione',
                'recommendation': [
                    'Crea pagine separate per: Home, Chi Siamo, Galleria, Servizi, Dintorni, Disponibilità, Contatti',
                    'Aggiungi pagina Recensioni/Testimonianze',
                    'Crea landing pages per periodi specifici (estate, inverno, eventi)',
                    'Pagina FAQ per domande comuni',
                    'Blog con guide turistiche della zona (Gallipoli, Salento)',
                ]
            })

            self.recommendations.append({
                'priority': 'CRITICA',
                'category': 'Website Structure',
                'title': 'Crea un sito multi-pagina completo',
                'actions': [
                    'Homepage: Hero image + USP + CTA prenotazione',
                    'Galleria: Minimo 15-20 foto HD della casa',
                    'Servizi: Elenca tutti i comfort (WiFi, AC, parcheggio, cucina)',
                    'Dintorni: Mappa interattiva, distanze da spiagge/ristoranti',
                    'Disponibilità: Calendario con prezzi per periodo',
                    'Recensioni: Testimonianze ospiti precedenti',
                    'Contatti: Form + WhatsApp + telefono + mappa',
                    'Chi Siamo: Storia della casa, perché sceglierci'
                ]
            })

        # No conversion tracking
        events = self.summary['content']['events']
        if 'contact_click' not in events and 'booking_click' not in events:
            self.recommendations.append({
                'priority': 'ALTA',
                'category': 'Conversion Tracking',
                'title': 'Implementa tracking conversioni',
                'actions': [
                    'Traccia click su numero di telefono',
                    'Traccia click su WhatsApp',
                    'Traccia submit form contatto',
                    'Traccia click su piattaforme booking (se presenti)',
                    'Imposta Goal in Google Analytics per conversioni',
                    'Aggiungi Facebook Pixel per retargeting',
                    'Monitora bounce rate per pagina'
                ]
            })

    def _analyze_traffic_sources(self):
        """Analyze traffic sources for vacation rental."""
        sources = self.summary['traffic_sources']
        percentages = sources['source_percentages']

        for source, percentage in percentages.items():
            if source == 'Direct' and percentage > 40:
                self.insights.append({
                    'area': 'Traffico Diretto',
                    'type': 'Clienti ricorrenti o passaparola',
                    'data': f'{percentage}% traffico diretto',
                    'meaning': 'Persone che conoscono già il brand o tornano da visite precedenti'
                })

            if source == 'Organic Search' and percentage < 10:
                self.warnings.append({
                    'area': 'Local SEO',
                    'severity': 'CRITICA',
                    'issue': f'Solo {percentage}% da ricerca organica',
                    'impact': 'Non appari quando cercano "casa vacanze Gallipoli"',
                    'recommendation': [
                        'Ottimizza per keywords locali: "casa vacanze Gallipoli", "affitto Baia Verde", "casa mare Salento"',
                        'Crea Google Business Profile (fondamentale per local SEO)',
                        'Registrati su TripAdvisor con recensioni',
                        'Ottimizza title: "Casa Vacanze Baia Verde Gallipoli - 200m dal Mare | 9 posti"',
                        'Meta description: location + USP + distanza mare + prezzo da',
                        'Schema.org markup: VacationRental, Place, Offer',
                        'Contenuto ricco con parole chiave locali'
                    ]
                })

                self.recommendations.append({
                    'priority': 'CRITICA',
                    'category': 'Local SEO',
                    'title': 'Piano SEO locale completo',
                    'actions': [
                        'Google Business Profile con foto, orari, descrizione',
                        'Registrazione su portali vacanze (Booking, Airbnb, Vrbo)',
                        'TripAdvisor listing con recensioni',
                        'Presenza su siti locali (Salento.it, ViaggiSalento, etc.)',
                        'Articoli blog su "Cosa fare a Gallipoli", "Le spiagge di Baia Verde"',
                        'Backlinks da blog turistici del Salento',
                        'Collaborazioni con attività locali (ristoranti, escursioni)',
                        'Directory turistiche (ENIT, regione Puglia)'
                    ]
                })

            if source == 'Organic Social':
                self.recommendations.append({
                    'priority': 'ALTA',
                    'category': 'Social Media Strategy',
                    'title': 'Ottimizza presenza social per turismo',
                    'actions': [
                        'Instagram: Foto professionali casa + paesaggi Salento',
                        'Facebook Page: Post regolari, recensioni, offerte',
                        'Pinterest: Board "Vacanze Salento", "Mare Puglia"',
                        'Hashtag: #Salento #Gallipoli #BaiaVerde #PugliaMare #CasaVacanze',
                        'Stories con esperienze ospiti (con permesso)',
                        'Reels/TikTok: Tour virtuale casa',
                        'Collabora con travel influencer del Salento',
                        'Condividi contenuto UGC (User Generated Content) ospiti'
                    ]
                })

    def _analyze_local_seo(self):
        """Analyze local SEO performance."""
        geo = self.summary['geography']

        italy_percentage = geo['country_percentages'].get('IT', 0)

        if italy_percentage < 60:
            self.insights.append({
                'area': 'Target Geografico',
                'type': 'Mercato internazionale',
                'data': f'Solo {italy_percentage}% utenti dall\'Italia',
                'opportunity': 'Opportunità di targeting internazionale'
            })

            self.recommendations.append({
                'priority': 'MEDIA',
                'category': 'Internazionalizzazione',
                'title': 'Espandi a mercati esteri',
                'actions': [
                    'Traduci sito in inglese (mercato US/UK)',
                    'Considera tedesco (mercato importante per Puglia)',
                    'Prezzi anche in EUR/USD/GBP',
                    'Presenza su Booking.com e Airbnb (fondamentale)',
                    'Targeting ads Facebook/Google su paesi chiave',
                    'Collabora con tour operator esteri',
                    'Partnership con voli low-cost per Brindisi/Bari'
                ]
            })
        else:
            self.recommendations.append({
                'priority': 'ALTA',
                'category': 'Marketing Locale',
                'title': 'Rafforza presenza mercato italiano',
                'actions': [
                    'Ads Google su keywords "weekend Salento", "affitto vacanze Puglia"',
                    'Facebook Ads targeting regioni del Nord Italia',
                    'Collaborazioni con travel blogger italiani',
                    'Offerte speciali per ponti e festività',
                    'Partnership con agenzie viaggi locali',
                    'Presenza su portali italiani (Homelidays, Trivago)'
                ]
            })

    def _analyze_content_completeness(self):
        """Analyze if website has complete information."""

        self.recommendations.append({
            'priority': 'CRITICA',
            'category': 'Content Must-Have',
            'title': 'Contenuti essenziali per conversione',
            'actions': [
                '📸 FOTO: Minimo 20 foto HD professionali (camere, esterni, zona giorno)',
                '💰 PREZZI: Prezzi chiari per stagione (alta/media/bassa)',
                '📅 DISPONIBILITÀ: Calendario online aggiornato in real-time',
                '⭐ RECENSIONI: Almeno 10 recensioni verificate (Google, TripAdvisor)',
                '📍 POSIZIONE: Mappa interattiva + indicazioni stradali',
                '🏖️ DINTORNI: Distanze da spiagge, ristoranti, supermercati, farmacia',
                '✨ SERVIZI: Lista dettagliata (WiFi, AC, TV, lavatrice, etc.)',
                '📏 SPAZI: Metratura, numero stanze, disposizione letti',
                '📞 CONTATTO: Telefono, WhatsApp, Email, Form',
                '📋 REGOLE: Check-in/out, animali, fumatori, etc.',
                '🎯 USP: Cosa rende unica la tua casa? (vista mare, giardino, parking)',
                '📖 GUIDA ZONA: Cosa vedere, dove mangiare, eventi locali'
            ]
        })

    def _analyze_geography_targeting(self):
        """Analyze geographic targeting opportunities."""
        geo = self.summary['geography']

        # High US traffic suggests opportunity
        us_percentage = geo['country_percentages'].get('US', 0)
        if us_percentage > 20:
            self.opportunities.append({
                'area': 'Mercato USA',
                'potential': 'Alto',
                'data': f'{us_percentage}% utenti dagli USA',
                'action': 'Mercato ricco, alta capacità di spesa'
            })

            self.recommendations.append({
                'priority': 'ALTA',
                'category': 'US Market',
                'title': 'Capitalizza interesse americano',
                'actions': [
                    'Traduzione completa in inglese (indispensabile)',
                    'Prezzi in USD oltre che EUR',
                    'Ads Google US su "Puglia vacation rental", "Italy beach house"',
                    'Presenza forte su Airbnb e VRBO (piattaforme US)',
                    'Contenuto adattato: unità di misura imperiali, AC (importante per USA)',
                    'Evidenzia connessioni aeroportuali (Brindisi/Bari)',
                    'Blog post "American\'s guide to Salento"',
                    'Partnership con influencer travel USA'
                ]
            })

    def _analyze_engagement(self):
        """Analyze user engagement."""
        engagement = self.summary['engagement']
        avg_time = engagement['avg_engagement_minutes']

        if avg_time < 2:
            self.warnings.append({
                'area': 'Engagement',
                'severity': 'ALTA',
                'issue': f'Tempo medio solo {avg_time:.2f} minuti',
                'impact': 'Utenti non esplorano abbastanza per prenotare',
                'recommendation': [
                    'Aggiungi virtual tour 360° della casa',
                    'Video walkthrough su YouTube e homepage',
                    'Galleria foto accattivante e facile da navigare',
                    'Mappa interattiva dei dintorni',
                    'Sezione "Esperienze" con storie ospiti',
                    'Blog con itinerari e guide locali',
                    'Ridimensiona pagine lunghe in sezioni navigabili',
                    'CTA chiari "Prenota ora" o "Richiedi disponibilità"'
                ]
            })

    def _analyze_seasonality(self):
        """Analyze and provide seasonality strategies."""

        self.recommendations.append({
            'priority': 'MEDIA',
            'category': 'Seasonal Strategy',
            'title': 'Strategia stagionale per affitti vacanze',
            'actions': [
                '☀️ ALTA STAGIONE (Giu-Set): Prezzi premium, min-stay 7 giorni',
                '🌸 MEDIA STAGIONE (Apr-Mag, Ott): Prezzi competitivi, promozioni weekend',
                '❄️ BASSA STAGIONE (Nov-Mar): Sconti long-stay, target digital nomads/pensionati',
                '🎄 FESTIVITÀ: Pacchetti speciali Natale/Capodanno/Pasqua',
                '📅 EARLY BOOKING: Sconto 15-20% per prenotazioni anticipate',
                '🔄 LAST MINUTE: Offerte settimana prima per riempire buchi',
                '💼 BUSINESS: Target long-stay lavoratori da remoto (inverno)',
                '🎉 EVENTI: Prezzi speciali per eventi locali (festival, concerti)'
            ]
        })

    def _analyze_competition(self):
        """Provide competitive analysis strategies."""

        self.recommendations.append({
            'priority': 'ALTA',
            'category': 'Competitive Advantage',
            'title': 'Differenziati dalla concorrenza',
            'actions': [
                '🔍 Analizza competitor su Booking/Airbnb (prezzi, servizi, recensioni)',
                '💎 Identifica il tuo USP: 200m dal mare è ottimo - ENFATIZZALO',
                '🏆 Supera competitor su: foto qualità, risposta rapida, flessibilità',
                '⚡ SERVIZI EXTRA: WiFi veloce, Netflix, barbecue, bici, beach kit',
                '🎁 WELCOME PACK: Vino locale, prodotti tipici, guida personale',
                '📱 TECNOLOGIA: Self check-in, app info casa, assistente virtuale',
                '🌟 RECENSIONI: Chiedi attivamente recensioni (incentiva con sconto futuro)',
                '💰 PREZZO: Posizionamento smart (non sempre il più basso)',
                '🤝 SERVIZI: Collaborazioni con chef privati, tour organizzati, transfer',
                '📸 CONTENUTO: Foto professionali > competitor (investimento essenziale)'
            ]
        })

    def _analyze_booking_platforms(self):
        """Recommend booking platform strategy."""

        self.recommendations.append({
            'priority': 'CRITICA',
            'category': 'Distribution Channels',
            'title': 'Presenza su piattaforme di prenotazione',
            'actions': [
                '🏨 BOOKING.COM: Essenziale, maggior traffico, commissione 15-18%',
                '🏠 AIRBNB: Fondamentale per mercato internazionale, commissione ~14%',
                '🌍 VRBO/HomeAway: Mercato USA/UK, famiglie, commissione o abbonamento',
                '✈️ TRIPADVISOR: Visibilità + recensioni (può linkare altri portali)',
                '🇮🇹 HOMELIDAYS: Mercato italiano ed europeo',
                '💻 SITO PROPRIO: Prenotazione diretta = zero commissioni (obiettivo finale)',
                '📊 STRATEGIA: Usa OTA per visibilità, converti su sito per margine',
                '🎯 PRICING: Parity rate tra piattaforme, incentiva booking diretto (sconto)',
                '📱 CHANNEL MANAGER: Software per gestire calendario multi-piattaforma',
                '💬 RISPOSTA: Velocità risposta <1h aumenta conversione del 30%'
            ]
        })

    def generate_priority_matrix(self) -> Dict:
        """Generate priority matrix for vacation rental business."""
        critical = [r for r in self.recommendations if r['priority'] == 'CRITICA']
        high_priority = [r for r in self.recommendations if r['priority'] == 'ALTA']
        medium_priority = [r for r in self.recommendations if r['priority'] == 'MEDIA']

        return {
            'critical': critical,
            'immediate_action': high_priority[:3],
            'short_term': medium_priority,
        }

    def generate_action_plan(self) -> str:
        """Generate vacation rental specific action plan."""
        plan = []

        plan.append("=" * 80)
        plan.append("PIANO D'AZIONE STRATEGICO - CASA DELLE MAGNOLIE")
        plan.append("Business: Affitto Turistico Vacanze - Baia Verde, Gallipoli")
        plan.append("=" * 80)
        plan.append("")

        # Executive Summary
        plan.append("EXECUTIVE SUMMARY")
        plan.append("-" * 80)
        plan.append(f"Analisi del periodo: {self.summary['period']['start']} - {self.summary['period']['end']}")
        plan.append(f"Utenti totali: {self.summary['users']['total_active_users']}")
        plan.append(f"Trend: {self.summary['users']['growth_trend'].upper()}")
        plan.append(f"Problemi critici: {len([w for w in self.warnings if w['severity'] == 'CRITICA'])}")
        plan.append(f"Opportunità identificate: {len(self.opportunities)}")
        plan.append("")

        plan.append("🎯 OBIETTIVO PRINCIPALE")
        plan.append("-" * 80)
        plan.append("Aumentare le prenotazioni dirette e la visibilità online per la stagione estiva")
        plan.append("")

        # Critical Issues
        critical_warnings = [w for w in self.warnings if w['severity'] == 'CRITICA']
        if critical_warnings:
            plan.append("🚨 PROBLEMI CRITICI (DA RISOLVERE IMMEDIATAMENTE)")
            plan.append("-" * 80)
            for idx, warning in enumerate(critical_warnings, 1):
                plan.append(f"\n{idx}. {warning['area']} - {warning['issue']}")
                plan.append(f"   ⚠️  Impatto: {warning['impact']}")
                plan.append(f"   Azioni:")
                for rec in warning['recommendation'][:5]:
                    plan.append(f"   • {rec}")
            plan.append("")

        # Key Insights
        if self.insights:
            plan.append("💡 INSIGHTS CHIAVE")
            plan.append("-" * 80)
            for idx, insight in enumerate(self.insights, 1):
                plan.append(f"{idx}. {insight['area']}: {insight['data']}")
            plan.append("")

        # Opportunities
        if self.opportunities:
            plan.append("🌟 OPPORTUNITÀ DI BUSINESS")
            plan.append("-" * 80)
            for opp in self.opportunities:
                plan.append(f"• {opp['area']}: {opp['data']} → {opp['action']}")
            plan.append("")

        # Priority Matrix
        matrix = self.generate_priority_matrix()

        plan.append("📋 PIANO D'AZIONE PRIORITIZZATO")
        plan.append("=" * 80)

        if matrix['critical']:
            plan.append("\n🔴 CRITICO - Questa settimana:")
            for idx, rec in enumerate(matrix['critical'], 1):
                plan.append(f"\n{idx}. {rec['category']}: {rec['title']}")
                for action in rec['actions'][:5]:
                    plan.append(f"   → {action}")

        if matrix['immediate_action']:
            plan.append("\n🟡 ALTA PRIORITÀ - Prossime 2-4 settimane:")
            for idx, rec in enumerate(matrix['immediate_action'], 1):
                plan.append(f"\n{idx}. {rec['category']}: {rec['title']}")
                for action in rec['actions'][:3]:
                    plan.append(f"   → {action}")

        if matrix['short_term']:
            plan.append("\n🟢 MEDIA PRIORITÀ - Prossimi 1-3 mesi:")
            for idx, rec in enumerate(matrix['short_term'], 1):
                plan.append(f"{idx}. {rec['title']}")

        plan.append("\n")
        plan.append("=" * 80)

        # Quick Wins for Vacation Rentals
        plan.append("\n⚡ QUICK WINS - Implementabili OGGI")
        plan.append("-" * 80)
        quick_wins = [
            "📸 Scatta almeno 10 nuove foto HD con smartphone (giornata di sole)",
            "📱 Aggiungi link WhatsApp cliccabile in homepage",
            "💰 Aggiungi prezzi indicativi per stagione",
            "⭐ Registrati su Google Business Profile (GRATIS e fondamentale)",
            "📝 Scrivi almeno 3 recensioni fittizie iniziali (chiedi ad amici/parenti reali)",
            "🗺️ Aggiungi Google Maps embed con posizione esatta",
            "📅 Crea calendario disponibilità (anche PDF inizialmente)",
            "✉️ Aggiungi form contatto semplice",
            "📍 Ottimizza title: 'Casa Vacanze Gallipoli Baia Verde 200m Mare | 9 posti'",
            "🔗 Crea profilo Instagram e posta 5 foto migliori casa"
        ]
        for win in quick_wins:
            plan.append(f"  {win}")

        plan.append("\n")
        plan.append("=" * 80)

        # ROI Expected
        plan.append("\n💰 STIMA IMPATTO ECONOMICO")
        plan.append("-" * 80)
        plan.append("Implementando le azioni CRITICHE + ALTA priorità:")
        plan.append("")
        plan.append("📈 Aumento traffico stimato: +200-300% (da ~30 a ~100 utenti/mese)")
        plan.append("🎯 Tasso conversione: 2-5% (2-5 richieste prenotazione per 100 visite)")
        plan.append("💵 Prenotazioni extra: +5-10 settimane/anno")
        plan.append("💰 Ricavo extra stimato: €3,500 - €7,000/anno")
        plan.append("")
        plan.append("Investimento necessario:")
        plan.append("  • Foto professionali: €150-300")
        plan.append("  • Traduzioni EN/DE: €200-400")
        plan.append("  • Ads Google/Facebook: €50-100/mese (stagionale)")
        plan.append("  • Booking platforms: 15% commissione solo su prenotazioni")
        plan.append("")
        plan.append("ROI stimato: 500-1000% nel primo anno")

        plan.append("\n" + "=" * 80)

        return "\n".join(plan)


def main():
    """Main execution."""
    import os

    print("\n" + "=" * 80)
    print("ANALISI STRATEGICA - CASA DELLE MAGNOLIE")
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
    analyzer = VacationRentalAnalyzer(summary)
    analyzer.analyze_all()
    analyzer._analyze_booking_platforms()

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
        'business_type': 'vacation_rental',
        'warnings': analyzer.warnings,
        'insights': analyzer.insights,
        'opportunities': analyzer.opportunities,
        'recommendations': analyzer.recommendations,
        'priority_matrix': analyzer.generate_priority_matrix()
    }

    json_file = "strategic_recommendations.json"
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(detailed_output, f, ensure_ascii=False, indent=2)

    print(f"💾 Raccomandazioni dettagliate salvate in: {json_file}\n")


if __name__ == "__main__":
    main()
