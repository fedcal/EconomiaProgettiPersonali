#!/usr/bin/env python3
"""
Script di migrazione dati da JSON a MySQL per Management Project Economy

Migra i dati finanziari dei tre progetti:
- FedericoCalo.dev (Freelance)
- CasaDelleMagnolie.com (Vacation Rental)
- PlayTheEvent.com (SaaS)

Author: Federico Calò
Version: 1.0.0
"""

import json
import mysql.connector
import os
from datetime import datetime
from decimal import Decimal
from pathlib import Path
from dotenv import load_dotenv

# Carica variabili d'ambiente
load_dotenv('../.env')

class DataMigrator:
    """Gestisce la migrazione dei dati JSON verso MySQL"""

    def __init__(self):
        """Inizializza la connessione al database"""
        self.db_config = {
            'host': 'localhost',
            'user': os.getenv('DB_USERNAME', 'root'),
            'password': os.getenv('DB_PASSWORD', ''),
            'database': 'management_economy'
        }

        self.connection = None
        self.cursor = None

        # Mapping categorie
        self.category_mapping = {
            'infrastructure': 'INFRASTRUCTURE',
            'branding': 'BRANDING',
            'content': 'CONTENT',
            'development': 'DEVELOPMENT',
            'marketing': 'MARKETING',
            'property': 'PROPERTY',
            'tools': 'TOOLS',
            'other': 'OTHER'
        }

        # Platform commission rates
        self.platform_commissions = {
            'Direct': 0.00,
            'Booking.com': 15.00,
            'Airbnb': 14.00,
            'VRBO': 12.00
        }

    def connect(self):
        """Stabilisce connessione con MySQL"""
        try:
            self.connection = mysql.connector.connect(**self.db_config)
            self.cursor = self.connection.cursor()
            print(f"✓ Connessione MySQL stabilita: {self.db_config['database']}")
        except mysql.connector.Error as err:
            print(f"✗ Errore connessione MySQL: {err}")
            raise

    def disconnect(self):
        """Chiude la connessione MySQL"""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        print("✓ Connessione MySQL chiusa")

    def load_json(self, file_path):
        """Carica dati da file JSON"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            print(f"✓ Caricato JSON: {file_path}")
            return data
        except FileNotFoundError:
            print(f"⚠ File non trovato: {file_path}")
            return None
        except json.JSONDecodeError as e:
            print(f"✗ Errore parsing JSON {file_path}: {e}")
            return None

    def insert_project(self, name, code, project_type, start_date, currency='EUR'):
        """Inserisce o aggiorna un progetto"""
        query_check = "SELECT id FROM projects WHERE code = %s"
        self.cursor.execute(query_check, (code,))
        result = self.cursor.fetchone()

        if result:
            project_id = result[0]
            print(f"  → Progetto '{name}' già esistente (ID: {project_id})")
            return project_id

        query = """
            INSERT INTO projects (name, code, type, start_date, currency, status, created_at, updated_at)
            VALUES (%s, %s, %s, %s, %s, 'ACTIVE', NOW(), NOW())
        """

        self.cursor.execute(query, (name, code, project_type, start_date, currency))
        self.connection.commit()
        project_id = self.cursor.lastrowid

        print(f"  ✓ Progetto creato: {name} (ID: {project_id})")
        return project_id

    def insert_one_time_cost(self, project_id, cost_data):
        """Inserisce un costo una tantum"""
        category = self.category_mapping.get(
            cost_data.get('category', 'other').lower(),
            'OTHER'
        )

        query = """
            INSERT INTO one_time_costs
            (project_id, name, amount, cost_date, category, description, payment_status, created_at, updated_at)
            VALUES (%s, %s, %s, %s, %s, %s, 'PAID', NOW(), NOW())
        """

        values = (
            project_id,
            cost_data['name'],
            cost_data['amount'],
            cost_data.get('date', datetime.now().strftime('%Y-%m-%d')),
            category,
            cost_data.get('description', '')
        )

        self.cursor.execute(query, values)
        print(f"    + Costo una tantum: {cost_data['name']} - €{cost_data['amount']}")

    def insert_recurring_cost(self, project_id, cost_data):
        """Inserisce un costo ricorrente"""
        category = self.category_mapping.get(
            cost_data.get('category', 'other').lower(),
            'OTHER'
        )

        frequency = cost_data.get('frequency', 'monthly').upper()
        if frequency not in ['MONTHLY', 'QUARTERLY', 'YEARLY']:
            frequency = 'MONTHLY'

        query = """
            INSERT INTO recurring_costs
            (project_id, name, amount, frequency, category, start_date, description,
             is_active, auto_renew, created_at, updated_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, TRUE, TRUE, NOW(), NOW())
        """

        values = (
            project_id,
            cost_data['name'],
            cost_data['amount'],
            frequency,
            category,
            cost_data.get('start_date', datetime.now().strftime('%Y-%m-%d')),
            cost_data.get('description', '')
        )

        self.cursor.execute(query, values)
        print(f"    + Costo ricorrente: {cost_data['name']} - €{cost_data['amount']}/{frequency.lower()}")

    def insert_revenue_stream(self, project_id, revenue_data):
        """Inserisce un flusso di ricavo"""
        revenue_type = revenue_data.get('type', 'other').upper()
        if revenue_type not in ['CONSULTATION', 'PROJECT', 'COURSE', 'PASSIVE', 'BOOKING', 'SUBSCRIPTION', 'OTHER']:
            revenue_type = 'OTHER'

        query = """
            INSERT INTO revenue_streams
            (project_id, name, amount, revenue_date, source, revenue_type,
             description, payment_status, created_at, updated_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, 'RECEIVED', NOW(), NOW())
        """

        values = (
            project_id,
            revenue_data['name'],
            revenue_data['amount'],
            revenue_data.get('date', datetime.now().strftime('%Y-%m-%d')),
            revenue_data.get('source', revenue_data.get('client', 'Unknown')),
            revenue_type,
            revenue_data.get('description', '')
        )

        self.cursor.execute(query, values)
        print(f"    + Revenue: {revenue_data['name']} - €{revenue_data['amount']}")

    def insert_booking(self, project_id, booking_data):
        """Inserisce una prenotazione (vacation rental)"""
        # Calcola commission rate
        platform = booking_data.get('platform', 'Direct')
        commission_rate = self.platform_commissions.get(platform, 15.00)

        price = Decimal(str(booking_data['price']))
        commission_amount = price * Decimal(str(commission_rate)) / Decimal('100')
        net_revenue = price - commission_amount

        # Calcola nights
        checkin = datetime.strptime(booking_data['checkin'], '%Y-%m-%d')
        checkout = datetime.strptime(booking_data['checkout'], '%Y-%m-%d')
        nights = (checkout - checkin).days

        price_per_night = price / Decimal(str(nights)) if nights > 0 else Decimal('0')

        query = """
            INSERT INTO bookings
            (project_id, checkin_date, checkout_date, guests, nights, price,
             price_per_night, platform, commission_rate, commission_amount,
             net_revenue, booking_status, guest_name, created_at, updated_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 'COMPLETED', %s, NOW(), NOW())
        """

        values = (
            project_id,
            booking_data['checkin'],
            booking_data['checkout'],
            booking_data.get('guests', 2),
            nights,
            float(price),
            float(price_per_night),
            platform,
            float(commission_rate),
            float(commission_amount),
            float(net_revenue),
            booking_data.get('guest_name', 'Guest')
        )

        self.cursor.execute(query, values)
        print(f"    + Prenotazione: {booking_data['checkin']} → {booking_data['checkout']} - €{price}")

    def migrate_project_federicocalo(self):
        """Migra dati FedericoCalo.dev"""
        print("\n📁 MIGRAZIONE: FedericoCalo.dev")
        print("=" * 50)

        json_path = Path(__file__).parent.parent.parent / 'Analisi Web Scraping progetti' / 'FedericoCalo' / 'financial_data.json'
        data = self.load_json(json_path)

        if not data:
            print("⚠ Nessun dato da migrare per FedericoCalo")
            return

        # Crea progetto
        project_id = self.insert_project(
            name='FedericoCalo.dev',
            code='FEDERICOCALO',
            project_type='FREELANCE',
            start_date=data.get('project_info', {}).get('start_date', '2020-01-01')
        )

        # Migra costi una tantum
        print("\n  Costi una tantum:")
        for cost in data.get('one_time_costs', []):
            self.insert_one_time_cost(project_id, cost)

        # Migra costi ricorrenti
        print("\n  Costi ricorrenti:")
        for cost in data.get('recurring_costs', []):
            self.insert_recurring_cost(project_id, cost)

        # Migra revenue streams
        print("\n  Revenue streams:")
        for revenue in data.get('revenue_streams', []):
            self.insert_revenue_stream(project_id, revenue)

        self.connection.commit()
        print(f"\n✓ FedericoCalo.dev migrato con successo")

    def migrate_project_casadellemagnolie(self):
        """Migra dati CasaDelleMagnolie.com"""
        print("\n📁 MIGRAZIONE: CasaDelleMagnolie.com")
        print("=" * 50)

        json_path = Path(__file__).parent.parent.parent / 'Analisi Web Scraping progetti' / 'CasaDelleMagnolie' / 'financial_data.json'
        data = self.load_json(json_path)

        if not data:
            print("⚠ Nessun dato da migrare per CasaDelleMagnolie")
            return

        # Crea progetto
        project_id = self.insert_project(
            name='CasaDelleMagnolie.com',
            code='CASADELLEMAGNOLIE',
            project_type='VACATION_RENTAL',
            start_date=data.get('project_info', {}).get('start_date', '2020-01-01')
        )

        # Migra costi una tantum
        print("\n  Costi una tantum:")
        for cost in data.get('one_time_costs', []):
            self.insert_one_time_cost(project_id, cost)

        # Migra costi ricorrenti
        print("\n  Costi ricorrenti:")
        for cost in data.get('recurring_costs', []):
            self.insert_recurring_cost(project_id, cost)

        # Migra prenotazioni
        print("\n  Prenotazioni:")
        for booking in data.get('bookings', []):
            self.insert_booking(project_id, booking)

        self.connection.commit()
        print(f"\n✓ CasaDelleMagnolie.com migrato con successo")

    def migrate_project_playtheevent(self):
        """Migra dati PlayTheEvent.com"""
        print("\n📁 MIGRAZIONE: PlayTheEvent.com")
        print("=" * 50)

        json_path = Path(__file__).parent.parent.parent / 'Analisi Web Scraping progetti' / 'PlayTheEvent' / 'financial_data.json'
        data = self.load_json(json_path)

        if not data:
            print("⚠ Nessun dato da migrare per PlayTheEvent (file non trovato o vuoto)")
            print("  Creazione progetto base...")

        # Crea progetto anche se non ci sono dati
        project_id = self.insert_project(
            name='PlayTheEvent.com',
            code='PLAYTHEEVENT',
            project_type='SAAS',
            start_date='2023-01-01'
        )

        if data:
            # Migra costi una tantum
            print("\n  Costi una tantum:")
            for cost in data.get('one_time_costs', []):
                self.insert_one_time_cost(project_id, cost)

            # Migra costi ricorrenti
            print("\n  Costi ricorrenti:")
            for cost in data.get('recurring_costs', []):
                self.insert_recurring_cost(project_id, cost)

            # Migra revenue streams
            print("\n  Revenue streams:")
            for revenue in data.get('revenue_streams', []):
                self.insert_revenue_stream(project_id, revenue)

        self.connection.commit()
        print(f"\n✓ PlayTheEvent.com migrato con successo")

    def run(self):
        """Esegue la migrazione completa"""
        print("\n" + "=" * 50)
        print("MIGRAZIONE DATI JSON → MySQL")
        print("Management Project Economy v1.0.0")
        print("=" * 50)

        try:
            self.connect()

            # Migra i tre progetti
            self.migrate_project_federicocalo()
            self.migrate_project_casadellemagnolie()
            self.migrate_project_playtheevent()

            print("\n" + "=" * 50)
            print("✓ MIGRAZIONE COMPLETATA CON SUCCESSO")
            print("=" * 50)

        except Exception as e:
            print(f"\n✗ ERRORE DURANTE LA MIGRAZIONE: {e}")
            if self.connection:
                self.connection.rollback()
            raise

        finally:
            self.disconnect()


if __name__ == '__main__':
    migrator = DataMigrator()
    migrator.run()
