"""
Fixtures modulari per test Formazing Bot.

Questo modulo importa e espone tutte le fixture dai file specializzati
per dominio, mantenendo la compatibilità con pytest.

STRUTTURA:
- telegram_fixtures.py: Fixture bot Telegram e training data
- notion_fixtures.py: Fixture base Notion (pages, responses)
- query_builder_fixtures.py: Fixture per query building
- crud_fixtures.py: Fixture per operazioni CRUD 
- client_fixtures.py: Fixture autenticazione e client
"""

# Import automatico di tutte le fixture per compatibilità pytest
from .telegram_fixtures import *
from .notion_fixtures import *
from .query_builder_fixtures import *
from .crud_fixtures import *
from .client_fixtures import *
from .facade_fixtures import *

__all__ = [
    # Telegram fixtures
    "mock_telegram_bot",
    "configured_telegram_service", 
    "sample_training_data",
    "alternative_training_data",
    "sample_feedback_data",
    
    # Notion base fixtures
    "sample_notion_page",
    "sample_notion_page_minimal", 
    "sample_notion_page_incomplete",
    "notion_query_response",
    "notion_page_malformed_date",
    "notion_page_rich_text_complex",
    "mock_notion_data_parser",
    "mock_notion_service",
    
    # QueryBuilder fixtures
    "sample_database_id",
    "expected_status_query",
    "expected_date_range_query", 
    "expected_area_query",
    "expected_combined_query",
    "invalid_query_samples",
    
    # CRUD fixtures
    "mock_notion_client",
    "sample_notion_id",
    "sample_update_response",
    "sample_retrieve_response",
    "sample_batch_formazioni_ids",
    "sample_multiple_fields_update",
    "mock_data_parser",
    "mock_api_error",
    
    # Client fixtures
    "valid_notion_token",
    "valid_database_id",
    "mock_notion_client_class",
    "mock_env_variables",
    "mock_env_missing_token",
    "mock_env_missing_database_id", 
    "mock_env_empty",
    
    # Facade fixtures
    "mock_notion_service_modules",
    "sample_facade_formazioni_response",
    "mock_notion_api_response",
    "facade_error_scenarios"
]