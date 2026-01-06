#!/usr/bin/env python3
"""
Script di test per verificare le credenziali Google Analytics
"""

import os
import sys

def test_credentials():
    """Test delle credenziali Google Analytics."""

    print("="*60)
    print("TEST CREDENZIALI GOOGLE ANALYTICS")
    print("="*60)
    print()

    # 1. Verifica file credenziali
    print("1. Verifica file credenziali...")

    credential_file = input("Inserisci il percorso del file JSON delle credenziali: ").strip()

    if not os.path.exists(credential_file):
        print(f"❌ ERRORE: File '{credential_file}' non trovato!")
        print("\nAssicurati di aver scaricato il file JSON e inserito il percorso corretto.")
        return False

    print(f"✅ File trovato: {credential_file}")
    print()

    # 2. Verifica contenuto JSON
    print("2. Verifica contenuto JSON...")
    try:
        import json
        with open(credential_file, 'r') as f:
            creds_data = json.load(f)

        required_fields = ['type', 'project_id', 'private_key', 'client_email']
        missing_fields = [field for field in required_fields if field not in creds_data]

        if missing_fields:
            print(f"❌ ERRORE: Campi mancanti nel JSON: {missing_fields}")
            return False

        print(f"✅ JSON valido")
        print(f"   Project ID: {creds_data['project_id']}")
        print(f"   Service Account: {creds_data['client_email']}")
        print()

        service_account_email = creds_data['client_email']

    except json.JSONDecodeError:
        print("❌ ERRORE: Il file non è un JSON valido!")
        return False
    except Exception as e:
        print(f"❌ ERRORE: {e}")
        return False

    # 3. Verifica librerie Python
    print("3. Verifica librerie Python...")
    try:
        from google.analytics.data_v1beta import BetaAnalyticsDataClient
        from google.analytics.data_v1beta.types import RunReportRequest
        print("✅ Librerie Google Analytics installate correttamente")
        print()
    except ImportError:
        print("❌ ERRORE: Librerie non installate!")
        print("\nEsegui: pip install google-analytics-data")
        return False

    # 4. Test connessione API
    print("4. Test connessione a Google Analytics...")
    property_id = input("Inserisci il PROPERTY ID di Google Analytics: ").strip()

    if not property_id:
        print("❌ Property ID non inserito!")
        return False

    try:
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_file

        client = BetaAnalyticsDataClient()

        request = RunReportRequest(
            property=f"properties/{property_id}",
            dimensions=[{"name": "date"}],
            metrics=[{"name": "activeUsers"}],
            date_ranges=[{"start_date": "7daysAgo", "end_date": "today"}],
        )

        response = client.run_report(request)

        print("✅ Connessione riuscita!")
        print()
        print("="*60)
        print("DATI ULTIMI 7 GIORNI")
        print("="*60)

        total_users = 0
        for row in response.rows:
            date = row.dimension_values[0].value
            users = int(row.metric_values[0].value)
            total_users += users
            print(f"Data: {date} - Utenti attivi: {users}")

        print("="*60)
        print(f"Totale utenti attivi (7 giorni): {total_users}")
        print("="*60)
        print()
        print("🎉 TUTTO FUNZIONA CORRETTAMENTE!")
        print()
        print("PROSSIMI PASSI:")
        print("1. Salva queste informazioni:")
        print(f"   - File credenziali: {credential_file}")
        print(f"   - Property ID: {property_id}")
        print(f"   - Service Account: {service_account_email}")
        print()
        print("2. Ricordati di dare accesso 'Viewer' al Service Account in Google Analytics!")
        print(f"   Email da aggiungere: {service_account_email}")
        print()

        return True

    except Exception as e:
        print(f"❌ ERRORE durante la connessione:")
        print(f"   {str(e)}")
        print()
        print("POSSIBILI CAUSE:")
        print("1. Non hai dato accesso al Service Account in Google Analytics")
        print(f"   Vai su Analytics > Admin > Property Access Management")
        print(f"   Aggiungi: {service_account_email} con ruolo 'Viewer'")
        print()
        print("2. Property ID errato")
        print("   Verifica in Analytics > Admin > Property Settings")
        print()
        print("3. API non abilitata")
        print("   Vai su Google Cloud Console > APIs & Services > Library")
        print("   Cerca 'Google Analytics Data API' e abilitala")

        return False


if __name__ == "__main__":
    print()
    success = test_credentials()
    print()

    if success:
        sys.exit(0)
    else:
        sys.exit(1)
