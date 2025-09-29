"""
Fixture per test NotionService (Facade).

Questo modulo contiene le fixture specifiche per il testing
del facade NotionService e integrazione moduli.

INCLUDE:
- Mock moduli NotionService
- Response simulate integrate
- Scenari errore facade
- Test dati end-to-end
"""

import pytest
from unittest.mock import Mock, patch, MagicMock


@pytest.fixture
def mock_notion_service_modules():
    """
    Mock completo moduli NotionService per test facade.
    
    Returns:
        Dict: Mock objects per tutti i moduli interni
    """
    with (
        patch('app.services.notion.NotionClient') as mock_client_class,
        patch('app.services.notion.NotionQueryBuilder') as mock_query_builder_class,
        patch('app.services.notion.NotionDataParser') as mock_data_parser_class,
        patch('app.services.notion.NotionCrudOperations') as mock_crud_class,
        patch('app.services.notion.NotionDiagnostics') as mock_diagnostics_class
    ):
        # Mock instances
        mock_client = Mock()
        mock_query_builder = Mock()
        mock_data_parser = Mock()
        mock_crud = Mock()
        mock_diagnostics = Mock()
        
        # Configure class mocks to return instances
        mock_client_class.return_value = mock_client
        mock_query_builder_class.return_value = mock_query_builder
        mock_data_parser_class.return_value = mock_data_parser
        mock_crud_class.return_value = mock_crud
        mock_diagnostics_class.return_value = mock_diagnostics
        
        # Configure client methods
        mock_client.get_database_id.return_value = "test-database-id"
        mock_client.get_client.return_value = Mock(databases=Mock())
        
        yield {
            'client': mock_client,
            'query_builder': mock_query_builder,
            'data_parser': mock_data_parser,
            'crud_operations': mock_crud,
            'diagnostics': mock_diagnostics,
            'client_class': mock_client_class,
            'query_builder_class': mock_query_builder_class,
            'data_parser_class': mock_data_parser_class,
            'crud_class': mock_crud_class,
            'diagnostics_class': mock_diagnostics_class
        }


@pytest.fixture
def sample_facade_formazioni_response():
    """
    Response simulata per metodi get_formazioni_* della facade.
    """
    return [
        {
            "id": "formazione-1",
            "nome": "Python Basics",
            "status": "Programmata",
            "area": "IT",
            "data_inizio": "2025-10-01",
            "docente": "Mario Rossi"
        },
        {
            "id": "formazione-2", 
            "nome": "Leadership Skills",
            "status": "Calendarizzata",
            "area": "HR",
            "data_inizio": "2025-10-15",
            "docente": "Laura Bianchi"
        }
    ]


@pytest.fixture
def mock_notion_api_response():
    """
    Mock response API Notion per test facade integration.
    """
    return {
        "object": "list",
        "results": [
            {
                "id": "page-1",
                "properties": {
                    "Nome": {"title": [{"text": {"content": "Python Basics"}}]},
                    "Status": {"status": {"name": "Programmata"}},
                    "Area": {"multi_select": [{"name": "IT"}]}
                }
            }
        ],
        "has_more": False
    }


@pytest.fixture
def facade_error_scenarios():
    """
    Scenari di errore per test facade error handling.
    """
    from notion_client.errors import APIResponseError
    
    return {
        'initialization_error': Exception("Errore inizializzazione moduli"),
        'api_error': APIResponseError(
            response=Mock(status_code=500, text='Server Error'),
            message="API Error",
            code="internal_server_error"
        ),
        'parsing_error': ValueError("Errore parsing dati Notion"),
        'validation_error': ValueError("Parametri invalidi")
    }


# Esporta tutti i fixture pubblici
__all__ = [
    "mock_notion_service_modules",
    "sample_facade_formazioni_response",
    "mock_notion_api_response", 
    "facade_error_scenarios"
]