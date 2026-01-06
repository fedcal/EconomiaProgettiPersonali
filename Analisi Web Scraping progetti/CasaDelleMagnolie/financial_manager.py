#!/usr/bin/env python3
"""
Financial Management System for Casa delle Magnolie
Vacation Rental Business - Seasonal revenue and occupancy tracking
"""

import json
from datetime import datetime, timedelta
from typing import Dict, List
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import sys
import os

# Add parent directory to path to import base class
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from FedericoCalo.financial_manager import FinancialManager


class VacationRentalFinancialManager(FinancialManager):
    """Extended financial manager for vacation rental business."""

    def __init__(self, project_name: str = "Casa delle Magnolie"):
        super().__init__(project_name)
        self.data['project_info']['type'] = 'Vacation Rental'
        self.data['bookings'] = []
        self.data['occupancy'] = {
            'total_weeks': 52,
            'booked_weeks': 0
        }

    def add_booking(self, checkin: str, checkout: str, guests: int, price: float, platform: str = "Direct"):
        """Add a booking/reservation."""
        # Calculate nights
        checkin_date = datetime.strptime(checkin, '%Y-%m-%d')
        checkout_date = datetime.strptime(checkout, '%Y-%m-%d')
        nights = (checkout_date - checkin_date).days

        booking = {
            'checkin': checkin,
            'checkout': checkout,
            'guests': guests,
            'nights': nights,
            'price': price,
            'price_per_night': round(price / nights, 2) if nights > 0 else 0,
            'platform': platform,
            'commission': self._calculate_commission(price, platform)
        }

        self.data['bookings'].append(booking)

        # Add as revenue stream
        net_revenue = price - booking['commission']
        self.add_revenue_stream(
            f"Prenotazione {checkin}",
            net_revenue,
            checkin,
            platform,
            'booking'
        )

        # Update occupancy
        weeks = nights / 7
        self.data['occupancy']['booked_weeks'] += weeks

    def _calculate_commission(self, price: float, platform: str) -> float:
        """Calculate platform commission."""
        commission_rates = {
            'Direct': 0.0,
            'Booking.com': 0.15,
            'Airbnb': 0.14,
            'VRBO': 0.12,
            'Homeaway': 0.12,
            'TripAdvisor': 0.13
        }

        rate = commission_rates.get(platform, 0.15)
        return round(price * rate, 2)

    def calculate_occupancy_rate(self) -> float:
        """Calculate occupancy percentage."""
        booked = self.data['occupancy']['booked_weeks']
        total = self.data['occupancy']['total_weeks']
        return round((booked / total * 100), 2) if total > 0 else 0

    def calculate_adr(self) -> float:
        """Calculate Average Daily Rate."""
        if not self.data['bookings']:
            return 0

        total_revenue = sum(b['price'] for b in self.data['bookings'])
        total_nights = sum(b['nights'] for b in self.data['bookings'])

        return round(total_revenue / total_nights, 2) if total_nights > 0 else 0

    def calculate_revpar(self) -> float:
        """Calculate Revenue Per Available Room (week in this case)."""
        total_revenue = sum(b['price'] for b in self.data['bookings'])
        total_weeks = self.data['occupancy']['total_weeks']

        return round(total_revenue / total_weeks, 2) if total_weeks > 0 else 0

    def get_seasonal_breakdown(self) -> Dict:
        """Breakdown revenue by season."""
        seasons = {
            'Alta Stagione (Giu-Set)': 0,
            'Media Stagione (Apr-Mag, Ott)': 0,
            'Bassa Stagione (Nov-Mar)': 0
        }

        for booking in self.data['bookings']:
            month = int(booking['checkin'].split('-')[1])

            if 6 <= month <= 9:
                seasons['Alta Stagione (Giu-Set)'] += booking['price']
            elif month in [4, 5, 10]:
                seasons['Media Stagione (Apr-Mag, Ott)'] += booking['price']
            else:
                seasons['Bassa Stagione (Nov-Mar)'] += booking['price']

        return seasons

    def get_platform_breakdown(self) -> Dict:
        """Breakdown by booking platform."""
        platforms = {}

        for booking in self.data['bookings']:
            platform = booking['platform']
            platforms[platform] = platforms.get(platform, 0) + booking['price']

        return platforms

    def generate_financial_report(self) -> str:
        """Generate vacation rental specific financial report."""
        report = []

        report.append("=" * 80)
        report.append(f"REPORT FINANZIARIO - {self.project_name}")
        report.append("Business Model: Affitto Turistico Vacanze")
        report.append("=" * 80)
        report.append(f"Data: {datetime.now().strftime('%Y-%m-%d')}")
        report.append("")

        # Financial Summary
        total_costs = self.calculate_total_costs()
        total_revenue = self.calculate_total_revenue()
        profit = self.calculate_profit()
        roi = self.calculate_roi()

        report.append("RIEPILOGO FINANZIARIO")
        report.append("-" * 80)
        report.append(f"Costi totali:    €{total_costs:,.2f}")
        report.append(f"Ricavi totali:   €{total_revenue:,.2f}")
        report.append(f"Profitto netto:  €{profit:,.2f}")
        report.append(f"ROI:             {roi:.2f}%")
        report.append("")

        # Vacation Rental Metrics
        occupancy = self.calculate_occupancy_rate()
        adr = self.calculate_adr()
        revpar = self.calculate_revpar()

        report.append("METRICHE VACATION RENTAL")
        report.append("-" * 80)
        report.append(f"Tasso di occupazione:           {occupancy:.2f}%")
        report.append(f"Settimane prenotate:            {self.data['occupancy']['booked_weeks']:.1f} / {self.data['occupancy']['total_weeks']}")
        report.append(f"ADR (Tariffa Media Giornaliera):€{adr:.2f}")
        report.append(f"RevPAR (Ricavo per Settimana):  €{revpar:.2f}")
        report.append(f"Numero prenotazioni:            {len(self.data['bookings'])}")
        report.append("")

        # Seasonal Breakdown
        seasonal = self.get_seasonal_breakdown()
        if seasonal and total_revenue > 0:
            report.append("DISTRIBUZIONE RICAVI PER STAGIONE")
            report.append("-" * 80)
            for season, amount in seasonal.items():
                percentage = (amount / total_revenue * 100) if total_revenue > 0 else 0
                report.append(f"{season:.<50} €{amount:>10,.2f} ({percentage:>5.1f}%)")
            report.append("")

        # Platform Breakdown
        platforms = self.get_platform_breakdown()
        if platforms:
            report.append("DISTRIBUZIONE RICAVI PER PIATTAFORMA")
            report.append("-" * 80)
            total_commissions = sum(b['commission'] for b in self.data['bookings'])

            for platform, amount in sorted(platforms.items(), key=lambda x: x[1], reverse=True):
                percentage = (amount / total_revenue * 100) if total_revenue > 0 else 0
                report.append(f"{platform:.<50} €{amount:>10,.2f} ({percentage:>5.1f}%)")

            report.append(f"\n{'Commissioni totali pagate':.<50} €{total_commissions:>10,.2f}")
            report.append("")

        # Cost Breakdown
        cost_breakdown = self.get_cost_breakdown()
        if cost_breakdown:
            report.append("BREAKDOWN COSTI PER CATEGORIA")
            report.append("-" * 80)
            for category, amount in sorted(cost_breakdown.items(), key=lambda x: x[1], reverse=True):
                percentage = (amount / total_costs * 100) if total_costs > 0 else 0
                report.append(f"{category:.<50} €{amount:>10,.2f} ({percentage:>5.1f}%)")
            report.append("")

        # Recurring Costs
        if self.data['recurring_costs']:
            report.append("COSTI OPERATIVI RICORRENTI")
            report.append("-" * 80)
            yearly_recurring = 0
            for cost in self.data['recurring_costs']:
                yearly = cost['amount']
                if cost['frequency'] == 'monthly':
                    yearly *= 12
                elif cost['frequency'] == 'quarterly':
                    yearly *= 4

                yearly_recurring += yearly
                report.append(f"{cost['name']:.<40} €{cost['amount']:>8,.2f}/{cost['frequency']:<10} (€{yearly:,.2f}/anno)")

            report.append(f"{'TOTALE COSTI ANNUALI':.<40} €{yearly_recurring:>8,.2f}")
            report.append("")

        # Target Analysis
        report.append("ANALISI OBIETTIVI")
        report.append("-" * 80)

        target_occupancy = 60  # Target 60% occupancy
        target_weeks = self.data['occupancy']['total_weeks'] * (target_occupancy / 100)
        current_weeks = self.data['occupancy']['booked_weeks']
        weeks_needed = target_weeks - current_weeks

        report.append(f"Obiettivo occupazione:          {target_occupancy}%")
        report.append(f"Occupazione attuale:            {occupancy:.2f}%")

        if weeks_needed > 0:
            report.append(f"Settimane da prenotare:         {weeks_needed:.1f}")
            potential_revenue = weeks_needed * 7 * adr if adr > 0 else 0
            report.append(f"Ricavo potenziale:              €{potential_revenue:,.2f}")
        else:
            report.append("✅ Obiettivo di occupazione raggiunto!")

        report.append("")

        # Recommendations
        report.append("RACCOMANDAZIONI STRATEGICHE")
        report.append("-" * 80)

        if occupancy < 40:
            report.append("⚠️  Occupazione bassa - Azioni suggerite:")
            report.append("   • Riduci prezzi in bassa stagione")
            report.append("   • Aumenta presenza su piattaforme (Booking, Airbnb)")
            report.append("   • Investi in marketing (Google Ads, Facebook)")
            report.append("   • Offerte last-minute")

        if len(self.data['bookings']) > 0:
            direct_bookings = len([b for b in self.data['bookings'] if b['platform'] == 'Direct'])
            direct_percentage = (direct_bookings / len(self.data['bookings']) * 100)

            if direct_percentage < 20:
                report.append("💡 Poche prenotazioni dirette - Suggerimenti:")
                report.append("   • Incentiva prenotazioni dirette (sconto 5-10%)")
                report.append("   • Migliora SEO locale")
                report.append("   • Sistema prenotazione online sul sito")

        report.append("")
        report.append("=" * 80)

        return "\n".join(report)


def create_sample_data_casadellemagnolie():
    """Create sample financial data for Casa delle Magnolie."""
    fm = VacationRentalFinancialManager("Casa delle Magnolie")

    # ONE-TIME COSTS (Setup e miglioramenti)
    fm.add_one_time_cost("Foto professionali", 250.00, "2025-03-01", "Marketing")
    fm.add_one_time_cost("Restyling arredamento", 1500.00, "2025-02-15", "Property")
    fm.add_one_time_cost("Nuovi elettrodomestici", 800.00, "2025-02-20", "Property")
    fm.add_one_time_cost("Traduzione sito EN/DE", 300.00, "2025-03-10", "Marketing")
    fm.add_one_time_cost("Biancheria nuova (lenzuola, asciugamani)", 400.00, "2025-03-01", "Property")

    # RECURRING COSTS
    fm.add_recurring_cost("Hosting sito web", 10.00, "monthly", "Infrastructure", "2025-01-01")
    fm.add_recurring_cost("Assicurazione casa vacanze", 45.00, "monthly", "Insurance", "2025-01-01")
    fm.add_recurring_cost("Pulizie dopo check-out", 80.00, "monthly", "Operations", "2025-04-01")  # Media 1/settimana in stagione
    fm.add_recurring_cost("Utenze (acqua, luce, gas)", 120.00, "monthly", "Utilities", "2025-01-01")
    fm.add_recurring_cost("Manutenzione ordinaria", 100.00, "monthly", "Maintenance", "2025-01-01")
    fm.add_recurring_cost("Internet/WiFi", 35.00, "monthly", "Utilities", "2025-01-01")

    # BOOKINGS (Stagione estiva + qualche booking fuori stagione)
    # Alta stagione (Luglio-Agosto)
    fm.add_booking("2025-07-05", "2025-07-12", 6, 1200.00, "Booking.com")
    fm.add_booking("2025-07-14", "2025-07-21", 8, 1400.00, "Airbnb")
    fm.add_booking("2025-07-23", "2025-07-30", 7, 1300.00, "Direct")
    fm.add_booking("2025-08-02", "2025-08-09", 6, 1350.00, "Booking.com")
    fm.add_booking("2025-08-11", "2025-08-18", 9, 1500.00, "Airbnb")
    fm.add_booking("2025-08-20", "2025-08-27", 8, 1450.00, "VRBO")

    # Giugno e Settembre (media stagione)
    fm.add_booking("2025-06-07", "2025-06-14", 6, 900.00, "Booking.com")
    fm.add_booking("2025-06-21", "2025-06-28", 5, 850.00, "Direct")
    fm.add_booking("2025-09-06", "2025-09-13", 6, 800.00, "Airbnb")

    # Pasqua (alta richiesta)
    fm.add_booking("2025-04-18", "2025-04-21", 8, 600.00, "Direct")  # 3 notti

    # Ponte 1 Maggio
    fm.add_booking("2025-05-01", "2025-05-04", 6, 500.00, "Booking.com")  # 3 notti

    return fm


def main():
    """Main execution."""
    import os

    print("\n" + "=" * 80)
    print("GESTIONE FINANZIARIA - CASA DELLE MAGNOLIE")
    print("=" * 80 + "\n")

    # Check if data file exists
    if os.path.exists("financial_data.json"):
        print("📂 Trovato file dati esistente")
        fm = VacationRentalFinancialManager()
        fm.load_from_json()
    else:
        print("📝 Creazione dati di esempio (stagione estiva)...")
        fm = create_sample_data_casadellemagnolie()
        fm.save_to_json()

    # Generate report
    report = fm.generate_financial_report()
    print(report)

    # Save report
    with open("financial_report.txt", 'w', encoding='utf-8') as f:
        f.write(report)
    print("\n💾 Report salvato in: financial_report.txt")

    # Create visualizations
    fm.create_visualizations()

    print("\n✅ Gestione finanziaria completata!\n")


if __name__ == "__main__":
    main()
