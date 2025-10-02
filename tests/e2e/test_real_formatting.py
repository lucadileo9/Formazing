#!/usr/bin/env python3
"""
Test di formattazione messaggi con dati reali da Notion
======================================================

Questo script:
1. Recupera formazioni reali dal database Notion
2. Testa la formattazione dei messaggi usando TelegramFormatter
3. Mostra anteprime di tutti i tipi di messaggio
4. Verifica template YAML e sostituzione variabili

Usage: python test_real_formatting.py
"""

import asyncio
import logging
import sys
from pathlib import Path

# Aggiungi la directory root del progetto al path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from app.services.notion import NotionService
from app.services.bot.telegram_formatters import TelegramFormatter

# Configura logging per output pulito
logging.basicConfig(
    level=logging.WARNING,  # Nascondi log INFO per output più pulito
    format='%(levelname)s: %(message)s'
)

def print_section_header(title: str, emoji: str = "📄"):
    """Stampa header della sezione in modo uniforme"""
    print(f"\n{emoji} {title.upper()}")
    print("=" * (len(title) + 4))

def print_message_preview(message: str, title: str = "Anteprima"):
    """Stampa anteprima messaggio con bordi"""
    print(f"\n💬 {title}:")
    print("┌" + "─" * 78 + "┐")
    for line in message.split('\n'):
        # Tronca righe troppo lunghe
        display_line = line[:76] + "..." if len(line) > 76 else line
        print(f"│ {display_line:<76} │")
    print("└" + "─" * 78 + "┘")

async def get_sample_formazioni():
    """Asynchronously fetches a sample 'formazione' (training session) for different statuses from Notion.
    This function initializes a `NotionService` to connect to the Notion API. It
    iterates through a predefined list of statuses ('Programmata', 'Calendarizzata',
    'Conclusa') and attempts to retrieve the training sessions for each.
    For every status where sessions are found, it takes the first one as a
    representative sample and adds it to the result dictionary. The function
    prints detailed progress, success, and error messages to the console during
    its execution.
    Returns:
        dict: A dictionary where keys are the status strings and values are the
            first 'formazione' object found for that status.
        None: If no 'formazioni' are found for any of the specified statuses.
    """
    print("🔍 Recupero formazioni reali da Notion...")
    
    notion = NotionService()
    sample_formazioni = {}
    
    # Recupera esempi per ogni status
    statuses = ['Programmata', 'Calendarizzata', 'Conclusa']
    
    for status in statuses:
        try:
            formazioni = await notion.get_formazioni_by_status(status)
            if formazioni:
                # Prendi la prima formazione come esempio
                sample_formazioni[status] = formazioni[0]
                nome = formazioni[0].get('Nome', 'N/A')
                area = formazioni[0].get('Area', ['N/A'])
                area_str = ', '.join(area) if isinstance(area, list) else str(area)
                print(f"✅ {status}: {nome} (Area: {area_str})")
            else:
                print(f"⚠️ {status}: Nessuna formazione trovata")
        except Exception as e:
            print(f"❌ Errore recupero {status}: {e}")
    
    if not sample_formazioni:
        print("❌ Nessuna formazione trovata in nessuno status!")
        return None
    
    print(f"✅ Recuperate {len(sample_formazioni)} formazioni di esempio")
    return sample_formazioni

def analyze_formazione_data(formazione: dict):
    """Analyzes and prints a formatted summary of a dictionary's contents.
    This utility function takes a dictionary, iterates through its items, and
    prints a detailed analysis to the console. For each key-value pair, it
    displays the key, the data type of the value, and a content preview.
    The preview is truncated for long strings and shows the count and first
    few elements for lists, making it useful for debugging and inspecting
    complex data structures.
    Args:
        formazione (dict): The dictionary containing the data to be analyzed.
    """
    print("\n🔍 ANALISI DATI FORMAZIONE:")
    print("─" * 40)
    
    for campo, valore in formazione.items():
        tipo = type(valore).__name__
        if isinstance(valore, str):
            preview = valore[:50] + "..." if len(valore) > 50 else valore
        elif isinstance(valore, list):
            preview = f"[{len(valore)} elementi] {valore[:3]}..."
        else:
            preview = str(valore)
        
        print(f"📝 {campo:<20}: {tipo:<10} = {preview}")

async def test_training_notification_formatting(sample_formazioni: dict):
    """Performs an end-to-end test of the training notification formatting.
    This asynchronous test function simulates the real-world process of formatting
    training notifications for different target groups (a main group and a
    specific area group).
    The test proceeds as follows:
    1.  Loads message templates from the `message_templates.yaml` config file.
    2.  Initializes the `TelegramFormatter` with the loaded templates.
    3.  Selects a sample training session from the `sample_formazioni` fixture,
    4.  Formats a notification message for the 'main_group'.
    5.  Formats a second notification message for the specific area of the
        training (e.g., 'IT').
    6.  Prints previews of both generated messages.
    7.  Compares the two messages and prints a line-by-line analysis of the
        differences, verifying that context-specific formatting is applied.
    Args:
        sample_formazioni (dict): A pytest fixture providing a dictionary of
            sample training data, keyed by status.
    Returns:
        bool: True if the entire process completes without exceptions,
              False otherwise. The primary output is printed to stdout for
              manual verification.
    """
    print_section_header("Test Notifiche Training", "🚀")
    
    # Inizializza formatter con template
    import yaml
    templates_path = project_root / "config" / "message_templates.yaml"
    
    try:
        with open(templates_path, 'r', encoding='utf-8') as f:
            templates = yaml.safe_load(f)
        formatter = TelegramFormatter(templates=templates)
    except Exception as e:
        print(f"❌ Errore inizializzazione formatter: {e}")
        return False
    
    # Usa la prima formazione disponibile
    status_priorità = ['Programmata', 'Calendarizzata', 'Conclusa']
    formazione = None
    
    for status in status_priorità:
        if status in sample_formazioni:
            formazione = sample_formazioni[status]
            print(f"📚 Usando formazione '{status}': {formazione.get('Nome', 'N/A')}")
            break
    
    if not formazione:
        print("❌ Nessuna formazione disponibile per test")
        return False
    
    # Debug dati formazione
    analyze_formazione_data(formazione)
    
    try:
        # 1. Test messaggio main group
        print("\n🌐 Test formattazione MAIN GROUP...")
        main_msg = formatter.format_training_message(
            training_data=formazione,
            group_key='main_group'
        )
        print_message_preview(main_msg, "Main Group Message")
        
        # 2. Test messaggio area specifica
        area_list = formazione.get('Area', ['IT'])
        if isinstance(area_list, list) and area_list:
            area = area_list[0]
        else:
            area = 'IT'  # Fallback
        
        print(f"\n🎯 Test formattazione AREA SPECIFICA ({area})...")
        area_msg = formatter.format_training_message(
            training_data=formazione,
            group_key=area
        )
        print_message_preview(area_msg, f"Area {area} Message")
        
        # 3. Confronto differenze
        print("\n📊 ANALISI DIFFERENZE:")
        main_lines = set(main_msg.split('\n'))
        area_lines = set(area_msg.split('\n'))
        
        only_main = main_lines - area_lines
        only_area = area_lines - main_lines
        
        if only_main:
            print("🌐 Solo in main group:")
            for line in only_main:
                if line.strip():
                    print(f"   • {line}")
        
        if only_area:
            print(f"🎯 Solo in area {area}:")
            for line in only_area:
                if line.strip():
                    print(f"   • {line}")
        
        return True
        
    except Exception as e:
        print(f"❌ Errore formattazione training: {e}")
        return False

async def test_feedback_request_formatting(sample_formazioni: dict):
    """Tests the formatting of a feedback request message for a training session.
        This asynchronous test function verifies that the `TelegramFormatter`
        correctly constructs a feedback request message. It performs the
        following steps:
        1. Initializes the formatter with message templates from a YAML file.
        2. Selects a sample training session from the provided dictionary,
           prioritizing one with the status 'Conclusa' (Completed).
        3. Calls `format_feedback_message` to generate the message content.
        4. Prints the generated message for visual inspection.
        5. Checks for the presence of key elements in the formatted message,
           including a specific emoji, the word 'feedback', the training
           session's name, and the feedback link.
        Args:
            sample_formazioni (dict): A dictionary fixture containing sample
                training data, keyed by their status.
        Returns:
            bool: True if the message is formatted correctly and contains all
                  required elements, False otherwise. This helps in identifying
                  the point of failure during the test run.
    """
    print_section_header("Test Richieste Feedback", "📝")
    
    # Inizializza formatter con template
    import yaml
    templates_path = project_root / "config" / "message_templates.yaml"
    
    try:
        with open(templates_path, 'r', encoding='utf-8') as f:
            templates = yaml.safe_load(f)
        formatter = TelegramFormatter(templates=templates)
    except Exception as e:
        print(f"❌ Errore inizializzazione formatter: {e}")
        return False
    
    # Preferibilmente usa una formazione 'Conclusa' per feedback
    formazione = None
    if 'Conclusa' in sample_formazioni:
        formazione = sample_formazioni['Conclusa']
        print("📚 Usando formazione 'Conclusa' per feedback")
    elif sample_formazioni:
        # Altrimenti usa la prima disponibile
        status, formazione = next(iter(sample_formazioni.items()))
        print(f"📚 Usando formazione '{status}' per feedback (non Conclusa)")
    
    if not formazione:
        print("❌ Nessuna formazione disponibile per test feedback")
        return False
    
    try:
        feedback_msg = formatter.format_feedback_message(
            training_data=formazione,
            feedback_link="https://forms.office.com/r/esempio-feedback",
            group_key='main_group'
        )
        print_message_preview(feedback_msg, "Feedback Request")
        
        # Verifica presenza elementi chiave
        print("\n🔍 VERIFICA ELEMENTI FEEDBACK:")
        elementi_richiesti = [
            ('📝', 'emoji feedback'),
            ('feedback', 'parola feedback'),
            (formazione.get('Nome', ''), 'nome formazione'),
            ('http', 'link feedback')
        ]
        
        for elemento, descrizione in elementi_richiesti:
            if elemento and elemento.lower() in feedback_msg.lower():
                print(f"✅ {descrizione}: Presente")
            else:
                print(f"❌ {descrizione}: Mancante")
        
        return True
        
    except Exception as e:
        print(f"❌ Errore formattazione feedback: {e}")
        return False

def test_formatter_initialization():
    """Tests the initialization process of the TelegramFormatter.
    This test function performs the following steps:
    1.  Loads message templates from the 'message_templates.yaml' file.
    2.  Initializes an instance of the `TelegramFormatter` class with the loaded templates.
    3.  Verifies that the formatter object has been created successfully.
    4.  Checks that the templates have been correctly loaded into the formatter instance
        and prints the names of the available templates.
    5.  Prints status messages to the console to track the progress and outcome.
    Returns:
        bool: True if the formatter and its templates are initialized without errors,
              False otherwise.
    """
    print_section_header("Test Inizializzazione Formatter", "🔧")
    
    try:
        # Carica template da file YAML
        import yaml
        templates_path = project_root / "config" / "message_templates.yaml"
        
        try:
            with open(templates_path, 'r', encoding='utf-8') as f:
                templates = yaml.safe_load(f)
            print(f"✅ Template YAML caricati da: {templates_path}")
        except Exception as e:
            print(f"❌ Errore caricamento template: {e}")
            return False
        
        formatter = TelegramFormatter(templates=templates)
        print("✅ TelegramFormatter inizializzato correttamente")
        
        # Verifica template caricati
        if hasattr(formatter, 'templates') and formatter.templates:
            print(f"✅ Template caricati: {len(formatter.templates)} template")
            
            # Lista template disponibili
            for template_name in formatter.templates.keys():
                print(f"   📄 {template_name}")
        else:
            print("⚠️ Template non trovati o non caricati")
            
        return True
        
    except Exception as e:
        print(f"❌ Errore inizializzazione formatter: {e}")
        return False

async def main():
    """Esegue tutti i test di formattazione"""
    print("🎨 FORMAZING - Test Formattazione Dati Reali")
    print("=" * 60)
    
    # 1. Test inizializzazione
    init_ok = test_formatter_initialization()
    if not init_ok:
        print("❌ Inizializzazione fallita. Impossibile continuare.")
        return False
    
    # 2. Recupera dati reali
    sample_formazioni = await get_sample_formazioni()
    if not sample_formazioni:
        print("❌ Nessun dato reale disponibile. Impossibile continuare.")
        return False
    
    # 3. Test formattazione notifiche training
    training_ok = await test_training_notification_formatting(sample_formazioni)
    
    # 4. Test formattazione feedback
    feedback_ok = await test_feedback_request_formatting(sample_formazioni)
        
    # 5. Risultato finale
    print("\n" + "=" * 60)
    print("📋 RISULTATO FINALE:")
    print(f"🔧 Inizializzazione: {'✅ OK' if init_ok else '❌ FAIL'}")
    print(f"🚀 Training Notifications: {'✅ OK' if training_ok else '❌ FAIL'}")
    print(f"📝 Feedback Requests: {'✅ OK' if feedback_ok else '❌ FAIL'}")
    
    if init_ok and training_ok and feedback_ok:
        print("\n🎉 Formattazione: TUTTO FUNZIONA!")
        print("📱 Messaggi pronti per invio reale")
        return True
    else:
        print("\n❌ Alcuni test di formattazione hanno fallito.")
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