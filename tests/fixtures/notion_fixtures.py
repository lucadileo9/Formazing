"""
Fixture base per test Notion.

Questo modulo contiene le fixture fondamentali per il testing
dei servizi Notion: pagine mock, responses API, parsers.

INCLUDE:
- Sample Notion pages (complete, minimal, incomplete)
- API responses
- Mock parsers
- Edge cases data
"""

import pytest
from unittest.mock import Mock
from tests.mocks.mock_notion import MockNotionService


@pytest.fixture
def mock_notion_service():
    """
    Istanza MockNotionService per test.
    Fornisce dati controllati e realistici.
    """
    return MockNotionService()


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


# Esporta tutti i fixture pubblici
__all__ = [
    "mock_notion_service",
    "sample_notion_page",
    "sample_notion_page_minimal",
    "sample_notion_page_incomplete", 
    "notion_query_response",
    "notion_page_malformed_date",
    "notion_page_rich_text_complex",
    "mock_notion_data_parser"
]