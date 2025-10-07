"""
Test Integrazione Completa: Notion → Microsoft → Notion

Questo script simula il workflow completo di calendarizzazione:
1. Recupera una formazione da Notion (stato "Programmata")
2. Crea evento Teams con Microsoft
3. Aggiorna Notion con link Teams e stato "Calendarizzata"

ATTENZIONE: Modifica DATI REALI in Notion e invia EMAIL REALI!

SUGGERIMENTO: Per test sicuri, crea una formazione in Notion con Area='Test'
              per inviare email solo a lucadileo@jemore.it invece che alle
              mailing list reali dei dipartimenti.

Uso:
    python test_notion_microsoft_integration.py
"""

import sys
import os
import asyncio

# Aggiungi root al path (tests/integration -> tests -> root)
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from config import Config
from app.services.notion import NotionService
from app.services.microsoft import MicrosoftService, MicrosoftServiceError


async def check_services():
    """Verifica che tutti i servizi siano configurati."""
    print("=" * 60)
    print("🔍 Verifico configurazione servizi...")
    print("=" * 60)
    
    validation = Config.validate_config()
    
    if not validation['notion']:
        print("❌ Notion non configurato!")
        return False
    
    if not validation['microsoft_graph']:
        print("❌ Microsoft Graph non configurato!")
        return False
    
    print("✅ Notion: OK")
    print("✅ Microsoft Graph: OK")
    return True


async def get_formazioni_programmata():
    """Recupera formazioni con stato 'Programmata' da Notion."""
    print("\n" + "=" * 60)
    print("📚 Recupero formazioni da Notion...")
    print("=" * 60)
    
    try:
        notion = NotionService()
        formazioni = await notion.get_formazioni_by_status("Programmata")
        
        if not formazioni:
            print("\n⚠️  Nessuna formazione con stato 'Programmata' trovata!")
            print("\n💡 Vai su Notion e crea una formazione con:")
            print("   - Nome: qualsiasi")
            print("   - Area: Test (per email di test a lucadileo@jemore.it)")
            print("   - Data: una data futura")
            print("   - Stato: Programmata")
            print("\n   ℹ️  Usa Area='Test' per test sicuri senza disturbare le mailing list reali.")
            return None
        
        print(f"\n✅ Trovate {len(formazioni)} formazioni programmate:")
        for i, f in enumerate(formazioni, 1):
            print(f"\n   [{i}] {f.get('Nome', 'N/A')}")
            print(f"       Codice: {f.get('Codice', 'N/A')}")
            print(f"       Area: {f.get('Area', 'N/A')}")
            print(f"       Data: {f.get('Data/Ora', 'N/A')}")
            print(f"       ID: {f.get('Id', 'N/A')}")
        
        return formazioni
        
    except Exception as e:
        print(f"\n❌ Errore recupero da Notion: {e}")
        import traceback
        traceback.print_exc()
        return None


async def calendarizza_formazione(formazione):
    """
    Calendarizza una formazione: crea evento Teams e aggiorna Notion.
    
    Simula il workflow di training_service.calendarizza_formazione()
    USA I NOMI DEI CAMPI NOTION (no mapping).
    """
    print("\n" + "=" * 60)
    print(f"📅 Calendarizzazione: {formazione['Nome']}")
    print("=" * 60)
    
    formazione_id = formazione['_notion_id']
    
    try:
        # 1. Crea evento Teams
        print("\n🔧 1. Creo evento Teams...")
        microsoft = MicrosoftService()
        
        # Passa i dati esattamente come vengono da Notion
        event_result = microsoft.calendar_operations.create_calendar_event(formazione)
        
        teams_link = event_result['teams_link']
        print(f"   ✅ Evento creato!")
        print(f"   📧 Email inviate a: {', '.join(event_result['attendee_emails'])}")
        print(f"   🔗 Teams link: {teams_link}")
        
        # 2. Aggiorna Notion
        print("\n🔧 2. Aggiorno Notion...")
        notion = NotionService()
        
        # Aggiornamento atomico: stato + link Teams in una chiamata
        await notion.update_formazione(formazione_id, {
            'Stato': 'Calendarizzata',
            'Link Teams': teams_link
        })
        
        print("   ✅ Notion aggiornato!")
        print(f"   - Stato → Calendarizzata")
        print(f"   - Link Teams salvato")
        
        # 3. Verifica aggiornamento
        print("\n🔧 3. Verifico aggiornamento...")
        # Ricarica formazione per verificare
        formazioni_updated = await notion.get_formazioni_by_status('Calendarizzata')
        formazione_updated = next(
            (f for f in formazioni_updated if f['_notion_id'] == formazione_id), 
            None
        )
        
        if formazione_updated:
            print(f"   ✅ Stato attuale: {formazione_updated.get('Stato')}")
            print(f"   ✅ Link Teams: {formazione_updated.get('Link Teams', 'N/A')[:50]}...")
        else:
            print(f"   ⚠️  Non riesco a rileggerela formazione, ma aggiornamento eseguito")
        
        return {
            'success': True,
            'event': event_result,
            'formazione_updated': formazione_updated
        }
        
    except MicrosoftServiceError as e:
        print(f"\n❌ Errore Microsoft: {e}")
        return {'success': False, 'error': str(e)}
    except Exception as e:
        print(f"\n❌ Errore imprevisto: {e}")
        import traceback
        traceback.print_exc()
        return {'success': False, 'error': str(e)}


async def main():
    """Esegue il test completo."""
    print("\n" + "=" * 60)
    print("🚀 TEST INTEGRAZIONE: Notion → Microsoft")
    print("=" * 60)
    
    # 1. Verifica configurazione
    if not await check_services():
        print("\n❌ Configurazione mancante. Verifica .env")
        return 1
    
    # 2. Recupera formazioni
    formazioni = await get_formazioni_programmata()
    if not formazioni:
        return 1
    
    # 3. Scegli formazione da calendarizzare
    print("\n" + "=" * 60)
    print("📝 Selezione formazione")
    print("=" * 60)
    
    if len(formazioni) == 1:
        formazione = formazioni[0]
        print(f"\n✅ Seleziono l'unica formazione: {formazione['Nome']}")
    else:
        print("\nQuale formazione vuoi calendarizzare?")
        scelta = input(f"Inserisci numero (1-{len(formazioni)}): ")
        
        try:
            idx = int(scelta) - 1
            if 0 <= idx < len(formazioni):
                formazione = formazioni[idx]
            else:
                print("❌ Scelta non valida")
                return 1
        except ValueError:
            print("❌ Inserisci un numero valido")
            return 1
    
    # 4. Mostra riepilogo
    print("\n" + "=" * 60)
    print("📋 RIEPILOGO OPERAZIONE")
    print("=" * 60)
    print(f"\n   Nome: {formazione['Nome']}")
    print(f"   Codice: {formazione['Codice']}")
    print(f"   Area: {', '.join(formazione['Area']) if isinstance(formazione['Area'], list) else formazione['Area']}")
    print(f"   Data: {formazione['Data/Ora']}")
    
    # Carica email dalla config
    import json
    with open('config/microsoft_emails.json', 'r') as f:
        emails = json.load(f)
    
    # Supporta multi-area
    areas = formazione['Area'] if isinstance(formazione['Area'], list) else [formazione['Area']]
    attendee_emails = []
    for area in areas:
        email = emails.get(area, emails.get('default'))
        if email not in attendee_emails:
            attendee_emails.append(email)
    
    print(f"\n   📧 Email saranno inviate a: {', '.join(attendee_emails)}")
    
    # 5. Chiedi conferma
    print("\n⚠️  ATTENZIONE:")
    print("   - Creerà un EVENTO REALE nel calendario")
    print("   - Invierà EMAIL REALE alla mailing list")
    print("   - Modificherà lo STATO in Notion → Calendarizzata")
    
    conferma = input("\n   Procedere? (scrivi 'SI' per confermare): ")
    
    if conferma.upper() != 'SI':
        print("\n❌ Operazione annullata.")
        return 0
    
    # 6. Esegui calendarizzazione
    result = await calendarizza_formazione(formazione)
    
    # 7. Risultato finale
    print("\n" + "=" * 60)
    if result['success']:
        print("✅ CALENDARIZZAZIONE COMPLETATA!")
        print("=" * 60)
        print("\n🎉 Operazione riuscita! Controlla:")
        print(f"   1. Email su: {', '.join(attendee_emails)}")
        print(f"   2. Calendario Outlook: lucadileo@jemore.it")
        print(f"   3. Notion: lo stato dovrebbe essere 'Calendarizzata'")
        print(f"   4. Teams link salvato in Notion")
        return 0
    else:
        print("❌ CALENDARIZZAZIONE FALLITA!")
        print("=" * 60)
        print(f"\nErrore: {result.get('error')}")
        return 1


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
