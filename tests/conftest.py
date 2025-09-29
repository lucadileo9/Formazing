"""
Configurazione pytest globale per test Formazing Bot.

Questo file definisce fixture condivise e configurazioni
per tutti i test del progetto.
Grazie a questo, i singoli file di test rimangono puliti
e focalizzati sulle logiche specifiche, senza questo file dovremmo in ogni
test caricare variabili ambiente, mockare dati, ecc.
"""

import pytest
import asyncio
import os
from unittest.mock import AsyncMock
from dotenv import load_dotenv

# Import moduli progetto
from tests.mocks.mock_notion import MockNotionService


@pytest.fixture(scope="session")
def event_loop():
    """
    Crea un event loop asyncio per tutti i test della sessione, necessario per test asincroni.
    Lo scope "session" significa che viene creato una volta per tutti i test.
    q: cos'è un event loop asyncio?
    a: Un event loop asyncio è un ciclo che gestisce l'esecuzione di operazioni asincrone
    in Python. Permette di eseguire funzioni in modo non bloccante, gestendo la concorrenza
    e le I/O in modo efficiente.
    """
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def load_test_env():
    """
    Carica variabili ambiente per test.
    Eseguito una volta per sessione. (scope="session")
    Restituisce dizionario con tutte le configurazioni necessarie
    """
    load_dotenv()
    return {
        'TELEGRAM_BOT_TOKEN': os.getenv('TELEGRAM_BOT_TOKEN'),
        'test_groups_config': 'tests/config/test_telegram_groups.json',
        'test_templates_config': 'tests/config/test_message_templates.yaml'
    }


@pytest.fixture
def mock_notion_service():
    """
    Istanza MockNotionService per test.
    Fornisce dati controllati e realistici.
    """
    return MockNotionService()


@pytest.fixture
def sample_training_data():
    """
    Dati formazione di esempio per test.
    Struttura standard usata in tutto il sistema.
    Data dinamica basata su oggi per funzionare sempre.
    """
    from datetime import datetime
    today = datetime.now()
    return {
        'Nome': 'Python Testing Masterclass',
        'Area': 'IT',
        'Data/Ora': today.strftime('%d/%m/%Y 14:30'),  # Data dinamica!
        'Codice': 'PY-TEST-001',
        'Link Teams': 'https://teams.microsoft.com/l/meetup-join/py-test-001',
        'Stato/Fase': 'Calendarizzata',
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
        'Stato/Fase': 'Completata'
    }


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


@pytest.fixture
def alternative_training_data():
    """
    Dati formazione alternativi per test multipli.
    Area diversa per testare targeting gruppi.
    """
    from datetime import datetime, timedelta
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


# ===== NOTION FIXTURES =====

@pytest.fixture
def sample_notion_page():
    """
    Pagina Notion mock completa per test parsing.
    Rappresenta una formazione tipica con tutti i campi popolati.
    """
    return {
        "id": "abc123-def456-ghi789",
        "properties": {
            "Nome": {
                "title": [{"plain_text": "Sicurezza Web Avanzata"}]
            },
            "Area": {
                "multi_select": [
                    {"name": "IT"}, 
                    {"name": "R&D"}
                ]
            },
            "Date": {
                "date": {"start": "2024-03-15T14:00:00.000Z"}
            },
            "Stato": {
                "status": {"name": "Programmata", "color": "blue"}
            },
            "Codice": {
                "rich_text": [{"plain_text": "IT-Sicurezza-2024-SPRING-01"}]
            },
            "Link Teams": {
                "url": "https://teams.microsoft.com/l/meetup-join/abc123"
            },
            "Periodo": {
                "select": {"name": "SPRING"}
            }
        }
    }


@pytest.fixture
def sample_notion_page_minimal():
    """
    Pagina Notion con solo campi obbligatori.
    Per testare comportamento con campi opzionali vuoti.
    """
    return {
        "id": "minimal-test-id",
        "properties": {
            "Nome": {
                "title": [{"plain_text": "Test Formazione Minimale"}]
            },
            "Area": {
                "multi_select": [{"name": "IT"}]
            },
            "Date": {
                "date": {"start": "2024-03-20T09:00:00.000Z"}
            },
            "Stato": {
                "status": {"name": "Calendarizzata", "color": "green"}
            },
            # Campi opzionali vuoti o nulli
            "Codice": {"rich_text": []},
            "Link Teams": {"url": None},
            "Periodo": {"select": None}
        }
    }


@pytest.fixture
def sample_notion_page_incomplete():
    """
    Pagina Notion con campi obbligatori mancanti.
    Per testare gestione errori e validazione.
    """
    return {
        "id": "incomplete-test-id",
        "properties": {
            "Nome": {
                "title": [{"plain_text": "Formazione Incompleta"}]
            },
            "Area": {
                "multi_select": []  # Area vuota - dovrebbe fallire
            },
            "Date": {
                "date": None  # Data mancante - dovrebbe fallire
            },
            "Stato": {
                "status": {"name": "Programmata", "color": "blue"}
            }
        }
    }


@pytest.fixture
def notion_query_response(sample_notion_page):
    """
    Response tipica da API Notion con formazioni multiple.
    Simula risultato reale da databases.query().
    """
    return {
        "results": [
            sample_notion_page,
            {
                "id": "second-formation-id",
                "properties": {
                    "Nome": {"title": [{"plain_text": "Marketing Digital Strategy"}]},
                    "Area": {"multi_select": [{"name": "Marketing"}]},
                    "Date": {"date": {"start": "2024-03-22T10:30:00.000Z"}},
                    "Stato": {"status": {"name": "Conclusa", "color": "red"}},
                    "Codice": {"rich_text": [{"plain_text": "MKT-Digital-2024-01"}]},
                    "Link Teams": {"url": "https://teams.microsoft.com/l/meetup-join/mkt123"},
                    "Periodo": {"select": {"name": "ONCE"}}
                }
            }
        ],
        "has_more": False,
        "next_cursor": None
    }


@pytest.fixture
def notion_page_malformed_date():
    """
    Pagina con data malformata per test edge cases.
    """
    return {
        "id": "malformed-date-id",
        "properties": {
            "Nome": {"title": [{"plain_text": "Test Data Malformata"}]},
            "Area": {"multi_select": [{"name": "IT"}]},
            "Date": {"date": {"start": "invalid-date-format"}},
            "Stato": {"status": {"name": "Programmata", "color": "blue"}}
        }
    }


@pytest.fixture
def notion_page_rich_text_complex():
    """
    Pagina con rich text complessi per test avanzati.
    """
    return {
        "id": "rich-text-id",
        "properties": {
            "Nome": {
                "title": [
                    {"plain_text": "Formazione "},
                    {"plain_text": "Multi-parte", "annotations": {"bold": True}}
                ]
            },
            "Area": {"multi_select": [{"name": "R&D"}, {"name": "IT"}, {"name": "HR"}]},
            "Date": {"date": {"start": "2024-04-01T15:45:00.000Z"}},
            "Stato": {"status": {"name": "Calendarizzata", "color": "green"}},
            "Codice": {
                "rich_text": [
                    {"plain_text": "COMP-"},
                    {"plain_text": "MULTI-2024", "annotations": {"code": True}}
                ]
            }
        }
    }


@pytest.fixture
def mock_notion_data_parser():
    """
    Mock del NotionDataParser per test che non vogliono testare parsing.
    """
    from unittest.mock import Mock
    parser = Mock()
    parser.parse_formazioni_list.return_value = [
        {
            'Nome': 'Mock Formazione',
            'Area': 'IT',
            'Data/Ora': '15/03/2024 14:00',
            'Stato/Fase': 'Programmata',
            'Codice': 'MOCK-001',
            'Link Teams': 'https://teams.microsoft.com/mock',
            'Periodo': 'SPRING',
            '_notion_id': 'mock-id-123'
        }
    ]
    parser.parse_single_formazione.return_value = parser.parse_formazioni_list.return_value[0]
    return parser
def pytest_configure(config):
    """
    Configurazione iniziale pytest.
    viene eseguito una volta all'avvio di pytest.
    Senza questo, i marker personalizzati non sarebbero riconosciuti
    q: cosa sono i marker personalizzati in pytest?
    a: I marker personalizzati in pytest sono etichette che puoi aggiungere ai tuoi test
    per categorizzarli o applicare comportamenti specifici. In questo caso, li usiamo per distinguere
    tra test che inviano messaggi reali su Telegram e test che usano solo mock.
    """
    # Registra marker personalizzati
    config.addinivalue_line(
        "markers", "real_telegram: test che inviano messaggi reali su Telegram"
    )
    config.addinivalue_line(
        "markers", "unit: test unitari veloci"
    )
    config.addinivalue_line(
        "markers", "integration: test di integrazione"
    )
    config.addinivalue_line(
        "markers", "mock_only: test solo con mock"
    )
    config.addinivalue_line(
        "markers", "notion: test per moduli NotionService"
    )


def pytest_collection_modifyitems(config, items):
    """
    Modifica raccolta test per aggiungere marker automatici.
    """
    for item in items:
        # Aggiungi marker automatici basati su path
        if "integration" in str(item.fspath):
            item.add_marker(pytest.mark.integration)
        if "unit" in str(item.fspath):
            item.add_marker(pytest.mark.unit)
        
        # Aggiungi marker per test che usano real_telegram_service
        if "real_telegram_service" in item.fixturenames:
            item.add_marker(pytest.mark.real_telegram)


def pytest_runtest_setup(item):
    """
    Setup per ogni test.
    Controlla prerequisiti per test reali.
    Si esegue PRIMA di ogni singolo test
    Controlla prerequisiti - se manca token, salta test reali
    Sicurezza automatica - evita crash per configurazioni mancanti
    Ad esempio una funzione con @pytest.mark.real_telegram controllerà presenza del token per evitare crash
    """
    # Skip test reali se manca token
    if "real_telegram" in [marker.name for marker in item.iter_markers()]:
        load_dotenv()
        if not os.getenv('TELEGRAM_BOT_TOKEN'):
            pytest.skip("TELEGRAM_BOT_TOKEN non trovato - Test reali saltati")


@pytest.fixture(autouse=True)
def setup_test_logging(caplog):
    """
    Setup logging per test.
    Cattura log per verifica.
    """
    import logging
    caplog.set_level(logging.INFO)


def pytest_report_header(config):
    """
    Header personalizzato per report pytest.
    """
    load_dotenv()
    token_status = "✅ Configurato" if os.getenv('TELEGRAM_BOT_TOKEN') else "❌ Mancante"
    
    return [
        "Formazing Bot Test Suite",
        f"TELEGRAM_BOT_TOKEN: {token_status}",
        "Uso: pytest -m 'real_telegram' per test con invio reale",
        "Uso: pytest -m 'not real_telegram' per test sicuri (default)"
    ]


# ===== FIXTURE PER QUERYBUILDER =====

@pytest.fixture
def sample_database_id():
    """Database ID standard per test query."""
    return "12345678-abcd-efgh-1234-567890abcdef"


@pytest.fixture
def expected_status_query():
    """Query attesa per filtro status."""
    return {
        "database_id": "test-db-id",
        "filter": {
            "property": "Stato",
            "status": {
                "equals": "Programmata"
            }
        },
        "sorts": [
            {
                "property": "Date",
                "direction": "ascending"
            }
        ],
        "page_size": 100
    }


@pytest.fixture
def expected_date_range_query():
    """Query attesa per range date."""
    return {
        "database_id": "test-db-id",
        "filter": {
            "and": [
                {
                    "property": "Date",
                    "date": {
                        "on_or_after": "2024-04-01"
                    }
                },
                {
                    "property": "Date", 
                    "date": {
                        "on_or_before": "2024-04-30"
                    }
                }
            ]
        },
        "sorts": [
            {
                "property": "Date",
                "direction": "ascending"
            }
        ]
    }


@pytest.fixture
def expected_area_query():
    """Query attesa per filtro area."""
    return {
        "database_id": "test-db-id",
        "filter": {
            "property": "Area",
            "multi_select": {
                "contains": "IT"
            }
        },
        "sorts": [
            {
                "property": "Date",
                "direction": "ascending"
            }
        ]
    }


@pytest.fixture
def expected_combined_query():
    """Query attesa per filtri combinati."""
    return {
        "database_id": "test-db-id",
        "filter": {
            "and": [
                {
                    "property": "Stato",
                    "status": {
                        "equals": "Programmata"
                    }
                },
                {
                    "property": "Area",
                    "multi_select": {
                        "contains": "IT"
                    }
                }
            ]
        },
        "sorts": [
            {
                "property": "Date",
                "direction": "ascending"
            }
        ]
    }


@pytest.fixture
def invalid_query_samples():
    """Esempi di query invalide per test validazione."""
    return {
        "missing_database_id": {
            "filter": {"property": "test"}
        },
        "empty_query": {},
        "none_query": None
    }