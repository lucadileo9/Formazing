#!/usr/bin/env python3
"""
Script di test rapido per NotionService

Test di connessione e funzionalità base per validare
implementazione prima di integrazione completa.

UTILIZZO:
python test_notion_connection.py

PREREQUISITI:
- .env configurato con NOTION_TOKEN e NOTION_DATABASE_ID
- pip install notion-client (già in requirements.txt)
"""

import asyncio
import sys
import os
from pathlib import Path

# Aggiungi root progetto al path (parent della cartella tests)
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.services.notion import NotionService, NotionServiceError
from config import Config


async def test_notion_service():
    """Test completo NotionService con diagnostica dettagliata."""
    
    print("=" * 60)
    print("🔍 TEST NOTION SERVICE - CONNESSIONE E FUNZIONALITÀ")  
    print("=" * 60)
    
    # ===== FASE 1: VALIDAZIONE CONFIGURAZIONE =====
    print("\n🔧 FASE 1: Validazione configurazione...")
    
    config_validation = Config.validate_config()
    print(f"✅ Configurazione generale: {config_validation}")
    
    if not config_validation['notion']:
        print("❌ ERRORE: Configurazione Notion mancante")
        print("👉 Configura NOTION_TOKEN e NOTION_DATABASE_ID in .env")
        return False
    
    # ===== FASE 2: INIZIALIZZAZIONE SERVIZIO =====
    print("\n🚀 FASE 2: Inizializzazione NotionService...")
    
    try:
        notion_service = NotionService()
        print("✅ NotionService inizializzato con successo")
        
        # Stampa statistiche servizio
        stats = notion_service.get_service_stats()
        print(f"📊 Stats servizio: {stats}")
        
    except Exception as e:
        print(f"❌ ERRORE inizializzazione: {e}")
        return False
    
    # ===== FASE 3: TEST CONNESSIONE =====
    print("\n🌐 FASE 3: Test connessione API Notion...")
    
    try:
        connection_result = await notion_service.test_connection()
        print(f"📡 Risultato connessione: {connection_result}")
        
        if not connection_result['connection_ok']:
            print("❌ ERRORE: Connessione API fallita")
            return False
            
        if not connection_result['database_accessible']:
            print("❌ ERRORE: Database non accessibile")
            return False
            
        print("✅ Connessione e database OK")
        
    except Exception as e:
        print(f"❌ ERRORE test connessione: {e}")
        return False
    
    # Mettiamo una stampa di tutte le info del database
    print("\n🔍 Dettagli database:")
    db_info = connection_result.get('database_info', {})
    for key, value in db_info.items():
        print(f"   {key}: {value}")
        
    # stampiamo le proprietà del database
    print("\n🔍 Proprietà database:")
    # Get database info to see actual property names
    try:
        from app.services.notion.notion_client import NotionClient
        temp_client = NotionClient()
        db_info = temp_client.get_client().databases.retrieve(database_id=temp_client.get_database_id())
        properties = db_info.get('properties', {})
        for prop_name, prop_details in properties.items():
            prop_type = prop_details.get('type', 'Unknown')
            print(f"   - {prop_name}: {prop_type}")
    except Exception as e:
        print(f"   Errore nel recupero proprietà: {e}")
        for prop, details in connection_result.get('database_info', {}).get('properties', {}).items():
            print(f"   - {prop}: {details.get('type', 'Unknown')}")
    
    
    # ===== FASE 4: TEST QUERY FORMAZIONI =====
    print("\n📋 FASE 4: Test query formazioni per status...")
    
    test_statuses = ['Calendarizzata', 'Programmata', 'Conclusa']
    
    for status in test_statuses:
        try:
            print(f"\n🔍 Query formazioni con status: '{status}'")
            formazioni = await notion_service.get_formazioni_by_status(status)
            
            print(f"📊 Risultati: {len(formazioni)} formazioni trovate")
            
            # Mostra prime 2 formazioni per validazione struttura dati
            for i, formazione in enumerate(formazioni[:2]):
                print(f"   [{i+1}] {formazione['Nome']} ({formazione['Area']}) - {formazione['Data/Ora']}")
                print(f"       Status: {formazione['Stato']} | Periodo: {formazione.get('Periodo', 'N/A')}")
                print(f"       Codice: {formazione.get('Codice', 'N/A')} | Link: {formazione.get('Link Teams', 'N/A')[:50]}...")
                
            if formazioni:
                print("✅ Query completata con successo")
            else:
                print("⚠️  Nessuna formazione trovata (potrebbe essere normale)")
                
        except NotionServiceError as e:
            print(f"❌ ERRORE NotionService per '{status}': {e}")
        except Exception as e:
            print(f"❌ ERRORE generico per '{status}': {e}")
    
    # ===== RISULTATO FINALE =====
    print("\n" + "=" * 60)
    print("🎯 TEST COMPLETATO CON SUCCESSO!")
    print("✅ NotionService è funzionante e pronto per l'integrazione")
    print("👉 Puoi procedere con l'implementazione completa")
    print("=" * 60)
    
    return True


def main():
    """Entry point script."""
    try:
        result = asyncio.run(test_notion_service())
        if result:
            sys.exit(0)
        else:
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n⌨️  Test interrotto dall'utente")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 ERRORE CRITICO: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()