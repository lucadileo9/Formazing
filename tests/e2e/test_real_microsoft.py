"""
Test Reale Microsoft Service - Crea un evento Teams di test.

ATTENZIONE: Questo script crea un VERO evento calendario e invia EMAIL REALI!

Uso:
    python test_real_microsoft.py

Cosa fa:
1. Verifica configurazione .env
2. Crea evento Teams con data/ora specificata
3. Invia email alla mailing list configurata (Area='Test' → lucadileo@jemore.it)
4. Stampa link Teams generato

NOTA: Usa Area='Test' per inviare email solo a lucadileo@jemore.it
      Modificala per testare altre mailing list.

Requisiti .env:
- MICROSOFT_TENANT_ID
- MICROSOFT_CLIENT_ID  
- MICROSOFT_CLIENT_SECRET
- MICROSOFT_USER_EMAIL
"""

import sys
import os
from datetime import datetime, timedelta

# Aggiungi root al path (tests/e2e -> tests -> root)
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from config import Config
from app.services.microsoft import MicrosoftService, MicrosoftServiceError


def check_env_config():
    """Verifica che tutte le variabili d'ambiente siano configurate."""
    print("=" * 60)
    print("🔍 Verifico configurazione...")
    print("=" * 60)
    
    validation = Config.validate_config()
    
    if not validation['microsoft_graph']:
        print("\n❌ Microsoft Graph NON configurato!")
        print("\nVariabili mancanti in .env:")
        
        if not Config.MICROSOFT_TENANT_ID:
            print("  ❌ MICROSOFT_TENANT_ID")
        if not Config.MICROSOFT_CLIENT_ID:
            print("  ❌ MICROSOFT_CLIENT_ID")
        if not Config.MICROSOFT_CLIENT_SECRET:
            print("  ❌ MICROSOFT_CLIENT_SECRET")
        if not Config.MICROSOFT_USER_EMAIL:
            print("  ❌ MICROSOFT_USER_EMAIL")
        
        print("\n📝 Aggiungi queste variabili nel file .env e riprova.")
        return False
    
    print("\n✅ Configurazione OK!")
    print(f"   Tenant ID: {Config.MICROSOFT_TENANT_ID[:8]}...")
    print(f"   User Email: {Config.MICROSOFT_USER_EMAIL}")
    return True


def create_test_event():
    """Crea un evento Teams di test."""
    print("\n" + "=" * 60)
    print("🧪 Creo evento Teams di TEST...")
    print("=" * 60)
    
    # Dati formazione di test - evento tra 5 minuti
    test_start = datetime.now() + timedelta(minutes=5)
    
    # USA I NOMI DEI CAMPI NOTION (con lettera maiuscola)
    formazione_test = {
        'Nome': '🧪 TEST - Formazione Microsoft Integration',
        'Codice': 'TEST-MSFT-2024-01',
        'Data/Ora': test_start.strftime('%d/%m/%Y %H:%M'),  # Formato Notion
        'Area': ['Test']  # Area "Test" → invia solo a lucadileo@jemore.it
    }
    
    print(f"\n📋 Dati evento:")
    print(f"   Nome: {formazione_test['Nome']}")
    print(f"   Codice: {formazione_test['Codice']}")
    print(f"   Data/Ora: {formazione_test['Data/Ora']}")
    print(f"   Area: {', '.join(formazione_test['Area'])}")
    
    # Chiedi conferma
    print("\n⚠️  ATTENZIONE: Questo creerà un VERO evento e invierà EMAIL REALI!")
    conferma = input("\n   Vuoi procedere? (scrivi 'SI' per confermare): ")
    
    if conferma.upper() != 'SI':
        print("\n❌ Test annullato dall'utente.")
        return None
    
    try:
        # Inizializza servizio
        print("\n🔧 Inizializzo Microsoft Service...")
        service = MicrosoftService()
        
        # Crea evento
        print("📅 Creo evento calendario...")
        result = service.calendar_operations.create_calendar_event(formazione_test)
        
        print("\n" + "=" * 60)
        print("✅ EVENTO CREATO CON SUCCESSO!")
        print("=" * 60)
        
        print(f"\n📧 Email inviate a: {', '.join(result.get('attendee_emails', []))}")
        print(f"📅 Event ID: {result.get('event_id')}")
        print(f"🔗 Teams Link: {result.get('teams_link')}")
        print(f"🌐 Calendar Link: {result.get('calendar_link')}")
        
        print("\n" + "=" * 60)
        print("✉️  VERIFICA LA TUA EMAIL!")
        print("=" * 60)
        print(f"\nLe email sono state inviate a: {', '.join(result.get('attendee_emails', []))}")
        print(f"Controlla la casella di queste mailing list.")
        print(f"\nL'evento inizia tra ~5 minuti ({test_start.strftime('%H:%M')})")
        print(f"Puoi unirti usando il link Teams sopra.")
        
        return result
        
    except MicrosoftServiceError as e:
        print(f"\n❌ ERRORE durante la creazione dell'evento:")
        print(f"   {e}")
        return None
    except Exception as e:
        print(f"\n❌ ERRORE IMPREVISTO:")
        print(f"   {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return None


def show_config_info():
    """Mostra informazioni sulla configurazione delle email."""
    print("\n" + "=" * 60)
    print("📋 Configurazione Email per Aree")
    print("=" * 60)
    
    try:
        import json
        with open('config/microsoft_emails.json', 'r') as f:
            emails = json.load(f)
        
        print("\nMapping Area → Email:")
        for area, email in emails.items():
            print(f"   {area:15} → {email}")
        
        print("\n💡 TIP: Modifica 'Area' nella funzione create_test_event()")
        print("         per testare email diverse (es. ['IT', 'R&D']).")
        print("         L'Area è una lista e supporta più destinatari.")
        print("\n   ℹ️  Attualmente configurato per usare Area='Test'")
        print("         che invia solo a lucadileo@jemore.it per test sicuri.")
        
    except Exception as e:
        print(f"⚠️  Non riesco a leggere config/microsoft_emails.json: {e}")


def main():
    """Esegue il test."""
    print("\n" + "=" * 60)
    print("🚀 TEST REALE - Microsoft Service")
    print("=" * 60)
    
    # 1. Verifica configurazione
    if not check_env_config():
        return 1
    
    # 2. Mostra configurazione email
    show_config_info()
    
    # 3. Crea evento test
    result = create_test_event()
    
    if result:
        print("\n" + "=" * 60)
        print("🎉 TEST COMPLETATO!")
        print("=" * 60)
        print("\n✅ Prossimi passi:")
        print("   1. Controlla l'email sulla mailing list")
        print("   2. Verifica che l'evento sia nel calendario di Outlook")
        print("   3. Prova a unirti al meeting Teams usando il link")
        print("\n   Se tutto funziona, l'integrazione è OK! 🚀")
        return 0
    else:
        print("\n" + "=" * 60)
        print("❌ TEST FALLITO")
        print("=" * 60)
        print("\nControlla:")
        print("   1. Le credenziali in .env sono corrette")
        print("   2. L'applicazione Azure ha i permessi necessari:")
        print("      - Calendars.ReadWrite")
        print("      - OnlineMeetings.ReadWrite")
        print("   3. I log sopra per dettagli sull'errore")
        return 1


if __name__ == "__main__":
    sys.exit(main())
