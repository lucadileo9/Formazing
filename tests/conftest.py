"""
Configurazione pytest globale per test Formazing Bot.

Questo file mantiene solo le fixture essenziali e globali,
mentre le fixture specifiche per dominio sono organizzate
nella directory tests/fixtures/ per modulo.

FIXTURE GLOBALI:
- event_loop: Session-level asyncio event loop
- load_test_env: Environment variables per test

FIXTURE MODULARIZZATE:
- tests/fixtures/telegram_fixtures.py
- tests/fixtures/notion_fixtures.py  
- tests/fixtures/query_builder_fixtures.py
- tests/fixtures/crud_fixtures.py
- tests/fixtures/client_fixtures.py
- tests/fixtures/facade_fixtures.py
"""

import pytest
import asyncio
import os
from unittest.mock import AsyncMock
from dotenv import load_dotenv

# Import moduli progetto
from tests.mocks.mock_notion import MockNotionService

# Import automatico di tutte le fixture modularizzate
from tests.fixtures import *


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
def mock_training_service():
    """
    Mock del training service per test integrati.
    Simula l'addestramento del bot con dati test.
    """
    service = AsyncMock()
    service.train.return_value = "Training completato con successo"
    service.get_training_status.return_value = "Trained"
    return service


@pytest.fixture
def test_config():
    """
    Configurazione test centralizzata.
    Fornisce percorsi e parametri standard per tutti i test.
    """
    return {
        'test_data_dir': 'tests/data',
        'timeout': 30,
        'max_retries': 3,
        'test_mode': True
    }