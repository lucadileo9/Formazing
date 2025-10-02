"""
Fixture per test NotionCrudOperations.

Questo modulo contiene le fixture specifiche per il testing
delle operazioni CRUD su Notion.

INCLUDE:
- Mock responses per operazioni CRUD
- Dati campione per update
- Batch operations 
- Gestione errori API
"""

import pytest
from unittest.mock import MagicMock


@pytest.fixture
def mock_notion_client():
    """Mock client Notion per test CRUD operations."""
    mock_client = MagicMock()
    mock_client.pages = MagicMock()
    mock_client.pages.update = MagicMock()
    mock_client.pages.retrieve = MagicMock()
    
    # Mock del wrapper client
    mock_wrapper = MagicMock()
    mock_wrapper.get_client.return_value = mock_client
    
    return mock_wrapper


@pytest.fixture
def sample_notion_id():
    """ID Notion standard per test."""
    return "12345678-abcd-efgh-ijkl-123456789abc"


@pytest.fixture
def sample_update_response():
    """Response simulata per update operations."""
    return {
        "object": "page",
        "id": "12345678-abcd-efgh-ijkl-123456789abc",
        "properties": {
            "Stato": {
                "status": {
                    "name": "Calendarizzata",
                    "color": "green"
                }
            }
        }
    }


@pytest.fixture
def sample_retrieve_response():
    """Response simulata per retrieve operation."""
    return {
        "object": "page",
        "id": "12345678-abcd-efgh-ijkl-123456789abc",
        "properties": {
            "Nome": {
                "title": [{"plain_text": "Test Formazione Retrieved"}]
            },
            "Area": {
                "multi_select": [{"name": "IT"}]
            },
            "Date": {
                "date": {"start": "2024-04-01T14:00:00.000Z"}
            },
            "Stato": {
                "status": {"name": "Programmata", "color": "blue"}
            },
            "Codice": {
                "rich_text": [{"plain_text": "TEST-RETRIEVED-01"}]
            },
            "Link Teams": {
                "url": "https://teams.microsoft.com/retrieved"
            },
            "Periodo": {
                "select": {"name": "SPRING"}
            }
        }
    }


@pytest.fixture
def sample_batch_formazioni_ids():
    """Lista di ID per test batch operations."""
    return [
        "batch-id-001",
        "batch-id-002", 
        "batch-id-003"
    ]


@pytest.fixture
def sample_multiple_fields_update():
    """Dati per test update multipli campi."""
    return {
        "Stato": "Calendarizzata",
        "Codice": "MULTI-UPDATE-2024-01",
        "Link Teams": "https://teams.microsoft.com/multi-update"
    }


@pytest.fixture
def mock_data_parser():
    """Mock parser per test retrieve operations."""
    parser = MagicMock()
    parser.parse_single_formazione.return_value = {
        "ID": "12345678-abcd-efgh-ijkl-123456789abc",
        "Nome": "Test Formazione Retrieved",
        "Area": "IT",
        "Data/Ora": "01/04/2024 15:00",
        "Stato": "Programmata",
        "Codice": "TEST-RETRIEVED-01",
        "Link Teams": "https://teams.microsoft.com/retrieved",
        "Periodo": "SPRING"
    }
    
    return parser


@pytest.fixture
def mock_api_error():
    """Mock APIResponseError per test gestione errori."""
    from notion_client.errors import APIResponseError
    
    # Crea un mock response con status_code
    mock_response = MagicMock()
    mock_response.status_code = 404
    mock_response.text = "Page not found"
    
    # Crea l'errore con il mock response e il code richiesto
    return APIResponseError(mock_response, "Test API Error", "test_error")


# Esporta tutti i fixture pubblici
__all__ = [
    "mock_notion_client",
    "sample_notion_id",
    "sample_update_response", 
    "sample_retrieve_response",
    "sample_batch_formazioni_ids",
    "sample_multiple_fields_update",
    "mock_data_parser",
    "mock_api_error"
]