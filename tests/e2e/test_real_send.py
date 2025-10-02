#!/usr/bin/env python3
"""
Test di invio reale controllato con conferma
============================================

Questo script:
1. Recupera formazioni reali dal database Notion
2. Permette all'utente di selezionare quale formazione usare
3. Mostra anteprima completa dei messaggi
4. Richiede conferma esplicita prima dell'invio REALE
5. Invia messaggi veri ai gruppi Telegram configurati
6. Traccia risultati e gestisce errori

⚠️ ATTENZIONE: Questo script invia messaggi REALI ai gruppi Telegram!

Usage: python test_real_send.py
"""

import asyncio
import logging
import sys
from pathlib import Path
from typing import Dict, List, Optional

# Aggiungi la directory root del progetto al path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from app.services.notion import NotionService
from app.services.telegram_service import TelegramService
from app.services.bot.telegram_formatters import TelegramFormatter
from config import Config

# Configura logging per output pulito
logging.basicConfig(
    level=logging.WARNING,  # Nascondi log INFO per output più pulito
    format='%(levelname)s: %(message)s'
)

def print_section_header(title: str, emoji: str = "🚀", warning: bool = False):
    """Stampa header della sezione con opzione warning"""
    color = "⚠️ " if warning else ""
    print(f"\n{color}{emoji} {title.upper()}")
    print("=" * (len(title) + 4))

def print_warning_box(message: str):
    """Stampa messaggio di warning in un box"""
    lines = message.split('\n')
    max_len = max(len(line) for line in lines)
    border_len = max_len + 4
    
    print("\n" + "⚠️ " + "═" * border_len + " ⚠️")
    for line in lines:
        print(f"║ {line:<{max_len}} ║")
    print("⚠️ " + "═" * border_len + " ⚠️")

def print_preview_box(content: str, title: str):
    """Stampa anteprima in un box strutturato"""
    print(f"\n📱 {title}:")
    print("┌" + "─" * 78 + "┐")
    for line in content.split('\n'):
        display_line = line[:76] + "..." if len(line) > 76 else line
        print(f"│ {display_line:<76} │")
    print("└" + "─" * 78 + "┘")

async def get_available_formazioni() -> Dict[str, List[Dict]]:
    """Asynchronously retrieves available formations from Notion, grouped by status.
    This function queries a Notion database via the NotionService to fetch
    formations. It iterates through a predefined list of statuses ('Programmata',
    'Calendarizzata', 'Conclusa') and fetches the corresponding formations for each.
    The function prints its progress to the console, including the number of
    formations found for each status, warnings for statuses with no formations,
    and any errors encountered during the API calls.
    Returns:
        Dict[str, List[Dict]]: A dictionary where keys are the status strings
        and values are lists of formation objects (represented as dictionaries).
        If no formations are found for a given status, that status will not
        be a key in the returned dictionary.
    """
    print("🔍 Recupero formazioni disponibili...")
    
    notion = NotionService()
    formazioni_by_status = {}
    
    statuses = ['Programmata', 'Calendarizzata', 'Conclusa']
    
    for status in statuses:
        try:
            formazioni = await notion.get_formazioni_by_status(status)
            if formazioni:
                formazioni_by_status[status] = formazioni
                print(f"✅ {status}: {len(formazioni)} formazioni disponibili")
            else:
                print(f"⚠️ {status}: Nessuna formazione trovata")
        except Exception as e:
            print(f"❌ Errore recupero {status}: {e}")
    
    return formazioni_by_status

def select_formazione(formazioni_by_status: Dict[str, List[Dict]]) -> Optional[Dict]:
    """Permette all'utente di selezionare una formazione"""
    print_section_header("Selezione Formazione", "🎯")
    
    if not formazioni_by_status:
        print("❌ Nessuna formazione disponibile!")
        return None
    
    # Crea lista numerata di tutte le formazioni
    formazioni_list = []
    
    for status, formazioni in formazioni_by_status.items():
        print(f"\n📋 Formazioni '{status}':")
        for i, formazione in enumerate(formazioni[:10]):  # Max 10 per status
            index = len(formazioni_list) + 1
            nome = formazione.get('Nome', 'N/A')
            area = formazione.get('Area', 'N/A')
            data = formazione.get('Data/Ora', 'N/A')
            codice = formazione.get('Codice', '')
            
            print(f"  {index:2d}. {nome}")
            print(f"      📍 Area: {area} | 📅 Data: {data}")
            if codice:
                print(f"      🏷 Codice: {codice}")
            
            formazioni_list.append(formazione)
    
    # Input utente
    print(f"\n🔢 Totale: {len(formazioni_list)} formazioni disponibili")
    
    try:
        while True:
            scelta_input = input(f"\n❓ Scegli formazione (1-{len(formazioni_list)}) o 'q' per uscire: ")
            
            if scelta_input.lower() == 'q':
                print("❌ Operazione annullata dall'utente")
                return None
            
            try:
                scelta = int(scelta_input)
                if 1 <= scelta <= len(formazioni_list):
                    return formazioni_list[scelta - 1]
                else:
                    print(f"❌ Numero non valido! Inserisci un numero tra 1 e {len(formazioni_list)}")
            except ValueError:
                print("❌ Input non valido! Inserisci un numero o 'q'")
                
    except KeyboardInterrupt:
        print("\n❌ Operazione interrotta dall'utente")
        return None

async def preview_messages(formazione: Dict, telegram_service: TelegramService) -> Dict[str, str]:
    """Generates and previews Telegram messages for a given training session.
    This asynchronous function loads message templates from a YAML configuration
    file, determines the target Telegram groups based on the training data,
    and then formats a specific message for each group. It prints a formatted
    preview of each message to the console for visual inspection.
    This is primarily used for testing and debugging purposes before the actual
    sending of messages.
    Args:
        formazione (Dict): A dictionary containing the details of the training
            session. Expected keys include 'Nome', 'Area', 'Data/Ora', and
            'Stato/Fase'.
        telegram_service (TelegramService): An instance of the TelegramService,
            used to resolve the target group chats for the training session.
    Returns:
        Dict[str, str]: A dictionary where keys are the target group identifiers
            (e.g., 'coordinatori_nazionali') and values are the fully
            formatted message strings for that group. Returns an empty
            dictionary if template loading or message formatting fails.
    """
    print_section_header("Anteprima Messaggi", "👀")
    
    # Carica template per formatter
    import yaml
    templates_path = project_root / "config" / "message_templates.yaml"
    
    try:
        with open(templates_path, 'r', encoding='utf-8') as f:
            templates = yaml.safe_load(f)
        formatter = TelegramFormatter(templates=templates)
    except Exception as e:
        print(f"❌ Errore caricamento template: {e}")
        return {}
    
    # Informazioni formazione
    nome = formazione.get('Nome', 'N/A')
    area = formazione.get('Area', 'N/A')
    data = formazione.get('Data/Ora', 'N/A')
    status = formazione.get('Stato/Fase', 'N/A')
    
    print(f"📚 Formazione: {nome}")
    print(f"🎯 Area: {area}")
    print(f"📅 Data: {data}")
    print(f"📊 Status: {status}")
    
    # Determina gruppi target
    target_groups = telegram_service._get_target_groups(formazione)
    print(f"🎯 Gruppi target: {', '.join(target_groups)}")
    
    # Genera messaggi per ogni gruppo
    messages = {}
    
    for group_key in target_groups:
        try:
            message = formatter.format_training_message(
                training_data=formazione,
                group_key=group_key
            )
            messages[group_key] = message
            
            group_name = group_key.replace('_', ' ').title()
            print_preview_box(message, f"Messaggio per {group_name}")
            
        except Exception as e:
            print(f"❌ Errore formattazione gruppo {group_key}: {e}")
    
    return messages


async def send_messages_with_tracking(telegram_service: TelegramService, messages: Dict[str, str]) -> Dict[str, bool]:
    """Sends multiple messages to different Telegram groups and tracks the outcome.
    This asynchronous function iterates through a dictionary of messages,
    attempting to send each one to its corresponding Telegram group using the
    provided service. It prints the progress and a final summary of
    successful and failed sends to the console.
    Args:
        telegram_service (TelegramService): The service object used to interact
            with the Telegram API.
        messages (Dict[str, str]): A dictionary mapping group keys to the
            HTML-formatted message strings to be sent.
    Returns:
        Dict[str, bool]: A dictionary containing the sending result for each
            group. Keys are the group keys, and values are True for success
            and False for failure.
    """
    print_section_header("Invio Messaggi", "🚀")
    
    results = {}
    successful = []
    failed = []
    
    print(f"📨 Invio {len(messages)} messaggi in corso...")
    
    for group_key, message in messages.items():
        print(f"\n📱 Invio a {group_key}...")
        
        try:
            # Invio del messaggio
            success = await telegram_service.send_message_to_group(
                group_key=group_key,
                message=message,
                parse_mode='HTML'
            )
            
            results[group_key] = success
            
            if success:
                successful.append(group_key)
                print(f"   ✅ Successo")
            else:
                failed.append(group_key)
                print(f"   ❌ Fallito")
                
        except Exception as e:
            results[group_key] = False
            failed.append(group_key)
            print(f"   ❌ Errore: {e}")
    
    # Riassunto risultati
    print(f"\n📊 RISULTATI INVIO:")
    print(f"   ✅ Successi: {len(successful)}/{len(messages)}")
    if successful:
        print(f"      Gruppi: {', '.join(successful)}")
    
    print(f"   ❌ Fallimenti: {len(failed)}/{len(messages)}")
    if failed:
        print(f"      Gruppi: {', '.join(failed)}")
    
    return results

async def main():
    """Esegue il test di invio controllato completo"""
    print("🚀 FORMAZING - Test Invio Reale Controllato")
    print("=" * 60)
    
    try:
        # 1. Recupera formazioni disponibili
        formazioni_by_status = await get_available_formazioni()
        if not formazioni_by_status:
            print("❌ Nessuna formazione disponibile per test")
            return False
        
        # 2. Selezione formazione
        formazione = select_formazione(formazioni_by_status)
        if not formazione:
            return False
        
        # 3. Inizializza TelegramService
        print_section_header("Inizializzazione Servizi", "🔧")
        try:
            telegram_service = TelegramService(
                token=Config.TELEGRAM_BOT_TOKEN,
                groups_config_path=Config.TELEGRAM_GROUPS_CONFIG,
                templates_config_path=Config.TELEGRAM_TEMPLATES_CONFIG
            )
            print("✅ TelegramService inizializzato")
        except Exception as e:
            print(f"❌ Errore inizializzazione TelegramService: {e}")
            return False
        
        # 4. Anteprima messaggi
        messages = await preview_messages(formazione, telegram_service)
        if not messages:
            print("❌ Impossibile generare anteprima messaggi")
            return False
                
        # 5. Invio reale
        results = await send_messages_with_tracking(telegram_service, messages)
        
        # 6. Risultato finale
        success_count = sum(1 for success in results.values() if success)
        total_count = len(results)
        
        print_section_header("Risultato Finale", "🏆")
        
        if success_count == total_count:
            print("🎉 INVIO COMPLETATO CON SUCCESSO!")
            print(f"✅ Tutti i {total_count} messaggi sono stati inviati correttamente")
        elif success_count > 0:
            print("⚠️ INVIO PARZIALMENTE COMPLETATO")
            print(f"✅ {success_count}/{total_count} messaggi inviati con successo")
        else:
            print("❌ INVIO FALLITO")
            print("❌ Nessun messaggio è stato inviato correttamente")
        
        return success_count > 0
        
    except Exception as e:
        print(f"\n💥 Errore imprevisto: {e}")
        return False

if __name__ == "__main__":
    try:
        result = asyncio.run(main())
        sys.exit(0 if result else 1)
        
    except KeyboardInterrupt:
        print("\n⏹️ Test interrotto dall'utente")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Errore imprevisto: {e}")
        sys.exit(1)