"""
Fixture per test NotionClient.

Questo modulo contiene le fixture specifiche per il testing
del client Notion e gestione environment.

INCLUDE:
- Mock client Notion
- Variabili d'ambiente per test
- Scenari errore configurazione
- Mock authentication
"""

import pytest
from unittest.mock import MagicMock, patch


@pytest.fixture
def valid_notion_token():
    """Token Notion valido per test."""
    return "secret_test-token-12345678-abcd-efgh-ijkl-123456789abc"


@pytest.fixture  
def valid_database_id():
    """Database ID valido per test."""
    return "12345678-abcd-efgh-ijkl-123456789abc"


@pytest.fixture
def mock_notion_client_class():
    """Mock della classe Client di notion-client."""
    with patch('app.services.notion.notion_client.Client') as mock_client_class:
        mock_client_instance = MagicMock()
        mock_client_class.return_value = mock_client_instance
        yield mock_client_class


@pytest.fixture
def mock_env_variables(valid_notion_token, valid_database_id):
    """Mock delle variabili d'ambiente per test."""
    env_vars = {
        'NOTION_TOKEN': valid_notion_token,
        'NOTION_DATABASE_ID': valid_database_id
    }
    
    with patch.dict('os.environ', env_vars):
        yield env_vars


@pytest.fixture
def mock_env_missing_token(valid_database_id):
    """Mock con token mancante per test errori."""
    env_vars = {
        'NOTION_DATABASE_ID': valid_database_id
        # NOTION_TOKEN mancante deliberatamente
    }
    
    with patch.dict('os.environ', env_vars, clear=True):
        yield env_vars


@pytest.fixture
def mock_env_missing_database_id(valid_notion_token):
    """Mock con database ID mancante per test errori."""
    env_vars = {
        'NOTION_TOKEN': valid_notion_token
        # NOTION_DATABASE_ID mancante deliberatamente  
    }
    
    with patch.dict('os.environ', env_vars, clear=True):
        yield env_vars


@pytest.fixture
def mock_env_empty():
    """Mock con tutte le variabili d'ambiente vuote."""
    with patch.dict('os.environ', {}, clear=True):
        yield {}


# Esporta tutti i fixture pubblici
__all__ = [
    "valid_notion_token",
    "valid_database_id", 
    "mock_notion_client_class",
    "mock_env_variables",
    "mock_env_missing_token",
    "mock_env_missing_database_id",
    "mock_env_empty"
]