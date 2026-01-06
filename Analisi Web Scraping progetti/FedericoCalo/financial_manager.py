#!/usr/bin/env python3
"""
Financial Management System for FedericoCalo.dev
Manages budget, costs, revenue, and ROI for professional portfolio/services business
"""

import json
import csv
from datetime import datetime, timedelta
from typing import Dict, List, Tuple
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


class FinancialManager:
    """Manage project finances, budget, and ROI."""

    def __init__(self, project_name: str = "FedericoCalo.dev"):
        self.project_name = project_name
        self.data = {
            'project_info': {
                'name': project_name,
                'type': 'Professional Portfolio & Services',
                'start_date': '2025-01-01',
                'currency': 'EUR'
            },
            'one_time_costs': [],
            'recurring_costs': [],
            'revenue_streams': [],
            'projections': []
        }

    def add_one_time_cost(self, name: str, amount: float, date: str, category: str):
        """Add a one-time expense."""
        self.data['one_time_costs'].append({
            'name': name,
            'amount': amount,
            'date': date,
            'category': category
        })

    def add_recurring_cost(self, name: str, amount: float, frequency: str, category: str, start_date: str):
        """Add a recurring expense (monthly, yearly, etc.)."""
        self.data['recurring_costs'].append({
            'name': name,
            'amount': amount,
            'frequency': frequency,  # 'monthly', 'yearly', 'quarterly'
            'category': category,
            'start_date': start_date
        })

    def add_revenue_stream(self, name: str, amount: float, date: str, source: str, type: str):
        """Add a revenue entry."""
        self.data['revenue_streams'].append({
            'name': name,
            'amount': amount,
            'date': date,
            'source': source,
            'type': type  # 'project', 'consultation', 'course', 'affiliate', etc.
        })

    def calculate_total_costs(self, start_date: str = None, end_date: str = None) -> float:
        """Calculate total costs in a period."""
        total = 0

        # One-time costs
        for cost in self.data['one_time_costs']:
            if start_date and end_date:
                if start_date <= cost['date'] <= end_date:
                    total += cost['amount']
            else:
                total += cost['amount']

        # Recurring costs (calculate for period)
        if start_date and end_date:
            start = datetime.strptime(start_date, '%Y-%m-%d')
            end = datetime.strptime(end_date, '%Y-%m-%d')
            months = (end.year - start.year) * 12 + (end.month - start.month)

            for cost in self.data['recurring_costs']:
                if cost['frequency'] == 'monthly':
                    total += cost['amount'] * months
                elif cost['frequency'] == 'yearly':
                    years = months / 12
                    total += cost['amount'] * years
                elif cost['frequency'] == 'quarterly':
                    quarters = months / 3
                    total += cost['amount'] * quarters

        return round(total, 2)

    def calculate_total_revenue(self, start_date: str = None, end_date: str = None) -> float:
        """Calculate total revenue in a period."""
        total = 0

        for revenue in self.data['revenue_streams']:
            if start_date and end_date:
                if start_date <= revenue['date'] <= end_date:
                    total += revenue['amount']
            else:
                total += revenue['amount']

        return round(total, 2)

    def calculate_profit(self, start_date: str = None, end_date: str = None) -> float:
        """Calculate profit (revenue - costs)."""
        revenue = self.calculate_total_revenue(start_date, end_date)
        costs = self.calculate_total_costs(start_date, end_date)
        return round(revenue - costs, 2)

    def calculate_roi(self, start_date: str = None, end_date: str = None) -> float:
        """Calculate ROI percentage."""
        costs = self.calculate_total_costs(start_date, end_date)
        profit = self.calculate_profit(start_date, end_date)

        if costs == 0:
            return 0

        roi = (profit / costs) * 100
        return round(roi, 2)

    def generate_monthly_forecast(self, months: int = 12) -> List[Dict]:
        """Generate monthly financial forecast."""
        forecast = []
        start = datetime.now()

        for i in range(months):
            month_date = start + timedelta(days=30 * i)
            month_str = month_date.strftime('%Y-%m')

            # Calculate monthly recurring costs
            monthly_costs = sum(
                cost['amount'] for cost in self.data['recurring_costs']
                if cost['frequency'] == 'monthly'
            )

            # Estimate monthly revenue (based on current average or projection)
            avg_monthly_revenue = self._estimate_monthly_revenue()

            forecast.append({
                'month': month_str,
                'costs': round(monthly_costs, 2),
                'revenue': round(avg_monthly_revenue, 2),
                'profit': round(avg_monthly_revenue - monthly_costs, 2)
            })

        return forecast

    def _estimate_monthly_revenue(self) -> float:
        """Estimate average monthly revenue."""
        if not self.data['revenue_streams']:
            return 0

        # Simple average for now
        total = sum(r['amount'] for r in self.data['revenue_streams'])
        months = 12  # Assume yearly
        return total / months

    def get_cost_breakdown(self) -> Dict:
        """Get costs broken down by category."""
        breakdown = {}

        # One-time costs
        for cost in self.data['one_time_costs']:
            cat = cost['category']
            breakdown[cat] = breakdown.get(cat, 0) + cost['amount']

        # Recurring costs (yearly equivalent)
        for cost in self.data['recurring_costs']:
            cat = cost['category']
            yearly_cost = cost['amount']

            if cost['frequency'] == 'monthly':
                yearly_cost *= 12
            elif cost['frequency'] == 'quarterly':
                yearly_cost *= 4

            breakdown[cat] = breakdown.get(cat, 0) + yearly_cost

        return {k: round(v, 2) for k, v in breakdown.items()}

    def get_revenue_breakdown(self) -> Dict:
        """Get revenue broken down by type."""
        breakdown = {}

        for revenue in self.data['revenue_streams']:
            rev_type = revenue['type']
            breakdown[rev_type] = breakdown.get(rev_type, 0) + revenue['amount']

        return {k: round(v, 2) for k, v in breakdown.items()}

    def generate_financial_report(self) -> str:
        """Generate comprehensive financial report."""
        report = []

        report.append("=" * 80)
        report.append(f"REPORT FINANZIARIO - {self.project_name}")
        report.append("=" * 80)
        report.append(f"Data: {datetime.now().strftime('%Y-%m-%d')}")
        report.append(f"Valuta: {self.data['project_info']['currency']}")
        report.append("")

        # Summary
        total_costs = self.calculate_total_costs()
        total_revenue = self.calculate_total_revenue()
        profit = self.calculate_profit()
        roi = self.calculate_roi()

        report.append("RIEPILOGO GENERALE")
        report.append("-" * 80)
        report.append(f"Costi totali:    €{total_costs:,.2f}")
        report.append(f"Ricavi totali:   €{total_revenue:,.2f}")
        report.append(f"Profitto:        €{profit:,.2f}")
        report.append(f"ROI:             {roi:.2f}%")
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

        # Revenue Breakdown
        revenue_breakdown = self.get_revenue_breakdown()
        if revenue_breakdown:
            report.append("BREAKDOWN RICAVI PER TIPO")
            report.append("-" * 80)
            for rev_type, amount in sorted(revenue_breakdown.items(), key=lambda x: x[1], reverse=True):
                percentage = (amount / total_revenue * 100) if total_revenue > 0 else 0
                report.append(f"{rev_type:.<50} €{amount:>10,.2f} ({percentage:>5.1f}%)")
            report.append("")

        # Recurring Costs
        if self.data['recurring_costs']:
            report.append("COSTI RICORRENTI")
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

            report.append(f"{'TOTALE ANNUALE':.<40} €{yearly_recurring:>8,.2f}")
            report.append("")

        # Monthly Forecast
        forecast = self.generate_monthly_forecast(6)
        if forecast:
            report.append("PREVISIONE 6 MESI")
            report.append("-" * 80)
            report.append(f"{'Mese':<12} {'Costi':>12} {'Ricavi':>12} {'Profitto':>12}")
            report.append("-" * 80)

            for month in forecast:
                report.append(
                    f"{month['month']:<12} "
                    f"€{month['costs']:>10,.2f} "
                    f"€{month['revenue']:>10,.2f} "
                    f"€{month['profit']:>10,.2f}"
                )

            total_forecast_profit = sum(m['profit'] for m in forecast)
            report.append("-" * 80)
            report.append(f"{'TOTALE 6 MESI':.<36} €{total_forecast_profit:>10,.2f}")
            report.append("")

        # Break-even analysis
        if total_costs > 0 and total_revenue > 0:
            months_to_breakeven = self._calculate_breakeven_months()
            report.append("ANALISI BREAK-EVEN")
            report.append("-" * 80)
            if months_to_breakeven:
                report.append(f"Mesi per raggiungere break-even: {months_to_breakeven:.1f} mesi")
                report.append(f"Data prevista break-even: {self._get_breakeven_date(months_to_breakeven)}")
            else:
                if profit > 0:
                    report.append("✅ Break-even già raggiunto!")
                else:
                    report.append("⚠️  Servono più dati per calcolare break-even")
            report.append("")

        report.append("=" * 80)

        return "\n".join(report)

    def _calculate_breakeven_months(self) -> float:
        """Calculate months needed to break even."""
        total_costs = self.calculate_total_costs()
        avg_monthly_revenue = self._estimate_monthly_revenue()

        if avg_monthly_revenue <= 0:
            return None

        monthly_costs = sum(
            cost['amount'] for cost in self.data['recurring_costs']
            if cost['frequency'] == 'monthly'
        )

        monthly_profit = avg_monthly_revenue - monthly_costs

        if monthly_profit <= 0:
            return None

        return total_costs / monthly_profit

    def _get_breakeven_date(self, months: float) -> str:
        """Get estimated break-even date."""
        start = datetime.strptime(self.data['project_info']['start_date'], '%Y-%m-%d')
        breakeven = start + timedelta(days=30 * months)
        return breakeven.strftime('%Y-%m-%d')

    def create_visualizations(self, output_prefix: str = "financial"):
        """Create financial visualization charts."""
        print("📊 Generazione grafici finanziari...")

        # 1. Costs vs Revenue
        self._plot_costs_vs_revenue(f"{output_prefix}_costs_vs_revenue.png")

        # 2. Cost breakdown pie
        self._plot_cost_breakdown(f"{output_prefix}_cost_breakdown.png")

        # 3. Revenue breakdown pie
        self._plot_revenue_breakdown(f"{output_prefix}_revenue_breakdown.png")

        # 4. Monthly forecast
        self._plot_monthly_forecast(f"{output_prefix}_forecast.png")

        print("✅ Grafici finanziari generati!")

    def _plot_costs_vs_revenue(self, filename: str):
        """Plot costs vs revenue comparison."""
        costs = self.calculate_total_costs()
        revenue = self.calculate_total_revenue()
        profit = self.calculate_profit()

        fig, ax = plt.subplots(figsize=(10, 6))

        categories = ['Costi', 'Ricavi', 'Profitto']
        values = [costs, revenue, profit]
        colors = ['#e74c3c', '#2ecc71', '#3498db']

        bars = ax.bar(categories, values, color=colors, alpha=0.7, edgecolor='black', linewidth=1.5)

        # Add value labels
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'€{height:,.0f}',
                   ha='center', va='bottom', fontweight='bold', fontsize=12)

        ax.set_ylabel('Euro (€)', fontsize=12)
        ax.set_title('Costi vs Ricavi vs Profitto', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3, axis='y')
        ax.axhline(y=0, color='black', linestyle='-', linewidth=0.5)

        plt.tight_layout()
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()

        print(f"  ✓ {filename}")

    def _plot_cost_breakdown(self, filename: str):
        """Plot cost breakdown pie chart."""
        breakdown = self.get_cost_breakdown()

        if not breakdown:
            print(f"  ⚠️  Nessun dato per breakdown costi")
            return

        fig, ax = plt.subplots(figsize=(10, 8))

        labels = list(breakdown.keys())
        sizes = list(breakdown.values())
        colors = plt.cm.Set3(range(len(labels)))

        wedges, texts, autotexts = ax.pie(
            sizes,
            labels=labels,
            colors=colors,
            autopct='%1.1f%%',
            startangle=90,
            textprops={'fontsize': 10}
        )

        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')

        ax.set_title('Breakdown Costi per Categoria', fontsize=14, fontweight='bold')

        plt.tight_layout()
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()

        print(f"  ✓ {filename}")

    def _plot_revenue_breakdown(self, filename: str):
        """Plot revenue breakdown pie chart."""
        breakdown = self.get_revenue_breakdown()

        if not breakdown:
            print(f"  ⚠️  Nessun dato per breakdown ricavi")
            return

        fig, ax = plt.subplots(figsize=(10, 8))

        labels = list(breakdown.keys())
        sizes = list(breakdown.values())
        colors = plt.cm.Set2(range(len(labels)))

        wedges, texts, autotexts = ax.pie(
            sizes,
            labels=labels,
            colors=colors,
            autopct='%1.1f%%',
            startangle=90,
            textprops={'fontsize': 10}
        )

        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')

        ax.set_title('Breakdown Ricavi per Tipo', fontsize=14, fontweight='bold')

        plt.tight_layout()
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()

        print(f"  ✓ {filename}")

    def _plot_monthly_forecast(self, filename: str):
        """Plot monthly forecast."""
        forecast = self.generate_monthly_forecast(12)

        if not forecast:
            print(f"  ⚠️  Nessun dato per forecast")
            return

        months = [f['month'] for f in forecast]
        costs = [f['costs'] for f in forecast]
        revenue = [f['revenue'] for f in forecast]
        profit = [f['profit'] for f in forecast]

        fig, ax = plt.subplots(figsize=(14, 6))

        x = range(len(months))
        width = 0.25

        ax.bar([i - width for i in x], costs, width, label='Costi', color='#e74c3c', alpha=0.7)
        ax.bar(x, revenue, width, label='Ricavi', color='#2ecc71', alpha=0.7)
        ax.bar([i + width for i in x], profit, width, label='Profitto', color='#3498db', alpha=0.7)

        ax.set_xlabel('Mese', fontsize=12)
        ax.set_ylabel('Euro (€)', fontsize=12)
        ax.set_title('Previsione Finanziaria 12 Mesi', fontsize=14, fontweight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels(months, rotation=45, ha='right')
        ax.legend()
        ax.grid(True, alpha=0.3, axis='y')
        ax.axhline(y=0, color='black', linestyle='-', linewidth=0.5)

        plt.tight_layout()
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()

        print(f"  ✓ {filename}")

    def save_to_json(self, filename: str = "financial_data.json"):
        """Save financial data to JSON."""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)
        print(f"💾 Dati salvati in {filename}")

    def load_from_json(self, filename: str = "financial_data.json"):
        """Load financial data from JSON."""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                self.data = json.load(f)
            print(f"✅ Dati caricati da {filename}")
        except FileNotFoundError:
            print(f"⚠️  File {filename} non trovato")


def create_sample_data_federicocalo():
    """Create sample financial data for FedericoCalo.dev."""
    fm = FinancialManager("FedericoCalo.dev")

    # ONE-TIME COSTS (Setup iniziale)
    fm.add_one_time_cost("Dominio .dev (3 anni)", 36.00, "2025-01-15", "Infrastructure")
    fm.add_one_time_cost("Logo Design", 150.00, "2025-01-20", "Branding")
    fm.add_one_time_cost("Foto professionali", 200.00, "2025-02-01", "Content")
    fm.add_one_time_cost("Template Premium", 79.00, "2025-01-10", "Development")

    # RECURRING COSTS
    fm.add_recurring_cost("Hosting VPS", 15.00, "monthly", "Infrastructure", "2025-01-01")
    fm.add_recurring_cost("Google Workspace", 6.00, "monthly", "Tools", "2025-01-01")
    fm.add_recurring_cost("Newsletter Service (Mailchimp)", 20.00, "monthly", "Marketing", "2025-03-01")
    fm.add_recurring_cost("SEO Tools (Ahrefs Lite)", 99.00, "monthly", "Marketing", "2025-04-01")
    fm.add_recurring_cost("Adobe Creative Cloud", 29.99, "monthly", "Tools", "2025-01-01")

    # REVENUE STREAMS (Proiezioni realistiche)
    # Consulenze
    fm.add_revenue_stream("Consulenza Web Dev - Cliente A", 1500.00, "2025-02-15", "Direct Client", "consultation")
    fm.add_revenue_stream("Consulenza SEO - Cliente B", 800.00, "2025-03-20", "Direct Client", "consultation")
    fm.add_revenue_stream("Sviluppo Sito - Cliente C", 3000.00, "2025-04-10", "Direct Client", "project")

    # Articoli/Tutorial
    fm.add_revenue_stream("Corso Online Udemy", 450.00, "2025-03-01", "Udemy", "course")
    fm.add_revenue_stream("Affiliate Marketing", 120.00, "2025-04-01", "Affiliate", "passive")

    return fm


def main():
    """Main execution."""
    import os

    print("\n" + "=" * 80)
    print("GESTIONE FINANZIARIA - FEDERICOCALO.DEV")
    print("=" * 80 + "\n")

    # Check if data file exists
    if os.path.exists("financial_data.json"):
        print("📂 Trovato file dati esistente")
        fm = FinancialManager()
        fm.load_from_json()
    else:
        print("📝 Creazione dati di esempio...")
        fm = create_sample_data_federicocalo()
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
