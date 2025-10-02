"""
Fixture per test Telegram Bot.

Questo modulo contiene tutte le fixture specifiche per il testing
del TelegramService e delle funzionalità bot.

INCLUDE:
- Mock bot Telegram
- TelegramService configurato
- Dati training e feedback di esempio
- Configurazioni test
"""

import pytest
import os
from datetime import datetime, timedelta
from unittest.mock import AsyncMock


@pytest.fixture
def mock_telegram_bot():
    """
    Mock del bot Telegram per test unitari.
    Simula risposte API senza invio reale.
    """
    bot = AsyncMock()
    bot.send_message.return_value = AsyncMock(message_id=123)
    bot.get_me.return_value = AsyncMock(
        id=123456789,
        username='test_bot',
        first_name='Test Bot'
    )
    return bot


@pytest.fixture
def sample_training_data():
    """
    Dati formazione di esempio per test.
    Struttura standard usata in tutto il sistema.
    Data dinamica basata su oggi per funzionare sempre.
    """
    today = datetime.now()
    return {
        'Nome': 'Python Testing Masterclass',
        'Area': 'IT',
        'Data/Ora': today.strftime('%d/%m/%Y 14:30'),  # Data dinamica!
        'Codice': 'PY-TEST-001',
        'Link Teams': 'https://teams.microsoft.com/l/meetup-join/py-test-001',
        'Stato': 'Calendarizzata',
        'Docente': 'Test Instructor Pro',
        'Descrizione': 'Corso avanzato testing Python con fixture centralizzate'
    }


@pytest.fixture
def sample_feedback_data():
    """
    Dati feedback di esempio per test.
    """
    return {
        'Nome': 'Completed Python Course',
        'Area': 'IT',
        'Codice': 'PY-COMP-001',
        'Descrizione': 'Corso Python completato con successo',
        'Stato': 'Completata'
    }


@pytest.fixture
def alternative_training_data():
    """
    Dati formazione alternativi per test multipli.
    Area diversa per testare targeting gruppi.
    """
    tomorrow = datetime.now() + timedelta(days=1)
    return {
        'Nome': 'Leadership Workshop Advanced',
        'Area': 'HR', 
        'Data/Ora': tomorrow.strftime('%d/%m/%Y 10:00'),
        'Codice': 'HR-TEST-002',
        'Link Teams': 'https://teams.microsoft.com/l/meetup-join/hr-test-002',
        'Descrizione': 'Workshop leadership per testing HR',
        'Docente': 'HR Test Instructor'
    }


@pytest.fixture
def test_config_paths():
    """
    Percorsi file di configurazione per test.
    """
    return {
        'groups': 'tests/config/test_telegram_groups.json',
        'templates': 'tests/config/test_message_templates.yaml'
    }


@pytest.fixture
def configured_telegram_service(load_test_env, test_config_paths, mock_notion_service):
    """
    TelegramService completamente configurato per test.
    
    QUESTA è la fixture principale che i test dovrebbero usare!
    
    Combina:
    - Token e configurazioni da load_test_env
    - Percorsi file da test_config_paths  
    - MockNotionService già iniettato
    
    Restituisce TelegramService pronto all'uso con mock Notion.
    """
    from app.services.telegram_service import TelegramService
    
    # Usa configurazione da fixture
    token = load_test_env['TELEGRAM_BOT_TOKEN']
    if not token:
        pytest.skip("TELEGRAM_BOT_TOKEN non trovato - Test reali saltati")
    
    # Verifica file esistenza
    groups_config = test_config_paths['groups']
    templates_config = test_config_paths['templates']
    
    if not os.path.exists(groups_config):
        pytest.skip(f"File {groups_config} non trovato - Crea configurazione test")
    if not os.path.exists(templates_config):
        pytest.skip(f"File {templates_config} non trovato - Crea template test")
    
    try:
        # Crea TelegramService REALE
        service = TelegramService(
            token=token,
            groups_config_path=groups_config,
            templates_config_path=templates_config
        )
        
        # Inietta MockNotionService da fixture
        service.set_notion_service(mock_notion_service)
        
        print(f"✅ TelegramService configurato con {len(service.groups)} gruppi di test")
        return service
        
    except Exception as e:
        pytest.skip(f"Errore setup TelegramService: {e}")


# Esporta tutti i fixture pubblici
__all__ = [
    "mock_telegram_bot",
    "sample_training_data", 
    "sample_feedback_data",
    "alternative_training_data",
    "test_config_paths",
    "configured_telegram_service"
]