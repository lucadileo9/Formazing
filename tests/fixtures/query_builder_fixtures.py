"""
Fixture per test NotionQueryBuilder.

Questo modulo contiene le fixture specifiche per il testing
della costruzione di query Notion.

INCLUDE:
- Database ID standard
- Query attese per diversi filtri
- Esempi query invalide
- Combinazioni query complesse
"""

import pytest


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


# Esporta tutti i fixture pubblici
__all__ = [
    "sample_database_id",
    "expected_status_query",
    "expected_date_range_query",
    "expected_area_query", 
    "expected_combined_query",
    "invalid_query_samples"
]