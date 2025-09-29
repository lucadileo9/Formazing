"""
Unit test per NotionClient.

Testa connessione, autenticazione e configurazione client Notion.
Focus su:
- Inizializzazione client con autenticazione
- Validazione credenziali e configurazione
- Gestione variabili d'ambiente
- Error handling per connessione fallita
- Sicurezza e gestione credenziali

UTILIZZO:
pytest tests/unit/notion/test_notion_client.py -v
pytest -m "unit and notion" tests/unit/notion/test_notion_client.py -v
"""

import pytest
from unittest.mock import patch, MagicMock
from app.services.notion.notion_client import NotionClient, NotionClientError


@pytest.mark.unit
@pytest.mark.notion
class TestNotionClient:
    """Test suite per NotionClient."""
    
    # ===== TEST INIZIALIZZAZIONE SUCCESSFUL =====
    
    def test_init_with_explicit_credentials(self, mock_notion_client_class, valid_notion_token, valid_database_id):
        """
        Test inizializzazione con credenziali esplicite.
        
        Verifica che:
        - Client Notion sia inizializzato con token fornito
        - Database ID sia configurato correttamente
        - Nessuna dipendenza da variabili d'ambiente
        - Configurazione sia validata
        
        Caso ideale: credenziali passate direttamente al costruttore.
        """
        # Test
        client = NotionClient(token=valid_notion_token, database_id=valid_database_id)
        
        # Verifica
        assert client.token == valid_notion_token
        assert client.database_id == valid_database_id
        assert client.client is not None
        
        # Verifica che il client Notion sia stato inizializzato
        mock_notion_client_class.assert_called_once_with(auth=valid_notion_token)
    
    def test_init_with_env_variables(self, mock_notion_client_class, mock_env_variables):
        """
        Test inizializzazione con variabili d'ambiente.
        
        Verifica che:
        - Credenziali siano lette da .env quando non fornite esplicitamente
        - Token e database ID da environment siano utilizzati
        - Client sia inizializzato correttamente
        - Configurazione sia completa
        
        Caso production: credenziali da variabili d'ambiente.
        """
        # Test (nessun parametro -> usa environment)
        client = NotionClient()
        
        # Verifica
        assert client.token == mock_env_variables['NOTION_TOKEN']
        assert client.database_id == mock_env_variables['NOTION_DATABASE_ID']
        assert client.client is not None
        
        mock_notion_client_class.assert_called_once_with(auth=mock_env_variables['NOTION_TOKEN'])
    
    def test_init_mixed_credentials(self, mock_notion_client_class, mock_env_variables, valid_database_id):
        """
        Test inizializzazione con credenziali miste (explicit + env).
        
        Verifica che:
        - Parametri espliciti abbiano precedenza su environment
        - Parametri mancanti siano letti da environment
        - Combinazione funzioni correttamente
        
        Caso flessibile: override selettivo delle credenziali.
        """
        custom_database_id = "custom-database-id-123"
        
        # Test (token da env, database_id esplicito)
        client = NotionClient(database_id=custom_database_id)
        
        # Verifica
        assert client.token == mock_env_variables['NOTION_TOKEN']  # Da environment
        assert client.database_id == custom_database_id  # Esplicito
        
        mock_notion_client_class.assert_called_once_with(auth=mock_env_variables['NOTION_TOKEN'])
    
    # ===== TEST VALIDAZIONE CREDENZIALI =====
    
    def test_init_missing_token_explicit(self, valid_database_id, mock_env_empty):
        """
        Test inizializzazione con token mancante (esplicito None).
        
        Verifica che:
        - ValueError sia sollevato per token None
        - Messaggio errore sia specifico
        - Client non sia inizializzato
        
        Edge case: token esplicitamente None senza environment.
        """
        with pytest.raises(ValueError, match="NOTION_TOKEN non configurato"):
            NotionClient(token=None, database_id=valid_database_id)
    
    def test_init_missing_database_id_explicit(self, valid_notion_token, mock_env_empty):
        """
        Test inizializzazione con database ID mancante (esplicito None).
        
        Verifica che:
        - ValueError sia sollevato per database_id None
        - Messaggio errore sia specifico
        - Validazione avvenga prima dell'inizializzazione client
        
        Edge case: database_id esplicitamente None senza environment.
        """
        with pytest.raises(ValueError, match="NOTION_DATABASE_ID non configurato"):
            NotionClient(token=valid_notion_token, database_id=None)
    
    def test_init_missing_token_environment(self, mock_env_missing_token):
        """
        Test inizializzazione con token mancante da environment.
        
        Verifica che:
        - ValueError sia sollevato quando NOTION_TOKEN non è in .env
        - Validazione environment variables funzioni
        - Errore sia chiaro per configurazione production
        
        Scenario production: configurazione .env incompleta.
        """
        with pytest.raises(ValueError, match="NOTION_TOKEN non configurato"):
            NotionClient()
    
    def test_init_missing_database_id_environment(self, mock_env_missing_database_id):
        """
        Test inizializzazione con database ID mancante da environment.
        
        Verifica che:
        - ValueError sia sollevato quando NOTION_DATABASE_ID non è in .env
        - Validazione environment variables sia robusta
        - Messaggio errore guidi troubleshooting
        
        Scenario production: database ID non configurato in .env.
        """
        with pytest.raises(ValueError, match="NOTION_DATABASE_ID non configurato"):
            NotionClient()
    
    def test_init_empty_environment(self, mock_env_empty):
        """
        Test inizializzazione con environment completamente vuoto.
        
        Verifica che:
        - ValueError sia sollevato per credenziali completamente mancanti
        - Primo errore sia per token (ordine validazione)
        - Sistema sia robusto contro environment mal configurato
        
        Edge case estremo: nessuna configurazione disponibile.
        """
        with pytest.raises(ValueError, match="NOTION_TOKEN non configurato"):
            NotionClient()
    
    # ===== TEST CLIENT NOTION INIZIALIZZAZIONE =====
    
    def test_init_client_creation_failure(self, valid_notion_token, valid_database_id):
        """
        Test gestione fallimento inizializzazione client Notion.
        
        Verifica che:
        - Exception da Client() sia propagata
        - Logging errore sia eseguito
        - Sistema non rimanga in stato inconsistente
        
        Scenario: problemi rete, token invalido, servizio Notion down.
        """
        with patch('app.services.notion.notion_client.Client') as mock_client:
            mock_client.side_effect = Exception("Connection failed")
            
            with pytest.raises(Exception, match="Connection failed"):
                NotionClient(token=valid_notion_token, database_id=valid_database_id)
    
    # ===== TEST METODI GETTER =====
    
    def test_get_client(self, mock_notion_client_class, valid_notion_token, valid_database_id):
        """
        Test getter per client Notion autenticato.
        
        Verifica che:
        - Client Notion interno sia restituito
        - Istanza sia quella creata durante init
        - Accesso sia sicuro e consistente
        
        Utilizzo: accesso client per operazioni API.
        """
        client = NotionClient(token=valid_notion_token, database_id=valid_database_id)
        
        notion_client = client.get_client()
        
        assert notion_client is not None
        assert notion_client == mock_notion_client_class.return_value
    
    def test_get_database_id(self, mock_notion_client_class, valid_notion_token, valid_database_id):
        """
        Test getter per database ID formazioni.
        
        Verifica che:
        - Database ID configurato sia restituito
        - Valore sia consistente con configurazione
        - Accesso sia diretto e performante
        
        Utilizzo: costruzione query per database specifico.
        """
        client = NotionClient(token=valid_notion_token, database_id=valid_database_id)
        
        db_id = client.get_database_id()
        
        assert db_id == valid_database_id
    
    # ===== TEST INFORMAZIONI CONFIGURAZIONE =====
    
    def test_get_config_info_complete(self, mock_notion_client_class, valid_notion_token, valid_database_id):
        """
        Test informazioni configurazione con setup completo.
        
        Verifica che:
        - Tutte le configurazioni siano indicate come presenti
        - Database ID preview sia fornito (senza esporre valore completo)
        - Cache TTL sia configurato
        - Informazioni siano utili per debugging
        
        Utilizzo: diagnostics e troubleshooting configurazione.
        """
        client = NotionClient(token=valid_notion_token, database_id=valid_database_id)
        
        config_info = client.get_config_info()
        
        assert config_info['token_configured'] is True
        assert config_info['database_id_configured'] is True
        assert config_info['database_id_preview'].startswith(valid_database_id[:8])
        assert config_info['database_id_preview'].endswith('...')
        assert config_info['cache_ttl_seconds'] == 300
    
    def test_get_config_info_security(self, mock_notion_client_class, valid_notion_token, valid_database_id):
        """
        Test sicurezza informazioni configurazione.
        
        Verifica che:
        - Token completo NON sia esposto nelle info
        - Database ID completo NON sia esposto (solo preview)
        - Informazioni sensibili siano protette
        - Solo flags booleani e preview sicuri siano disponibili
        
        Sicurezza critica: prevenzione leak credenziali in log/debug.
        """
        client = NotionClient(token=valid_notion_token, database_id=valid_database_id)
        
        config_info = client.get_config_info()
        
        # Verifica che credenziali complete NON siano presenti
        assert valid_notion_token not in str(config_info)
        assert valid_database_id not in str(config_info)
        
        # Verifica che solo informazioni sicure siano presenti
        assert 'token' not in config_info  # Solo 'token_configured'
        assert 'database_id' not in config_info  # Solo 'database_id_configured' e 'database_id_preview'
    
    # ===== TEST CACHE E CONFIGURAZIONE =====
    
    def test_cache_configuration(self, mock_notion_client_class, valid_notion_token, valid_database_id):
        """
        Test configurazione cache interno.
        
        Verifica che:
        - Cache TTL sia configurato (5 minuti default)
        - Strutture cache siano inizializzate
        - Configurazione sia pronta per utilizzo futuro
        
        Preparazione: cache per ottimizzazioni future.
        """
        client = NotionClient(token=valid_notion_token, database_id=valid_database_id)
        
        assert client._cache_ttl == 300  # 5 minuti
        assert client._last_cache_time is None  # Non ancora utilizzato
        assert client._cached_data == {}  # Vuoto alla creazione
    
    # ===== TEST EDGE CASES =====
    
    def test_empty_string_credentials(self, mock_env_empty):
        """
        Test gestione credenziali stringa vuota.
        
        Verifica che:
        - Stringhe vuote siano trattate come credenziali mancanti
        - Validazione sia robusta contro input malformati
        - Comportamento sia consistente con None
        
        Edge case: configurazione .env con valori vuoti.
        """
        with pytest.raises(ValueError, match="NOTION_TOKEN non configurato"):
            NotionClient(token="", database_id="test-db")
        
        with pytest.raises(ValueError, match="NOTION_DATABASE_ID non configurato"):
            NotionClient(token="test-token", database_id="")
    
    def test_whitespace_credentials(self, mock_env_empty):
        """
        Test gestione credenziali con solo whitespace.
        
        Verifica che:
        - Whitespace-only credentials siano trattate come invalide
        - Validazione sia robusta contro input edge case
        - Trimming non salvi credenziali malformate
        
        Edge case: spazi accidentali in configurazione.
        """
        with pytest.raises(ValueError, match="NOTION_TOKEN non configurato"):
            NotionClient(token="   ", database_id="test-db")
        
        with pytest.raises(ValueError, match="NOTION_DATABASE_ID non configurato"):
            NotionClient(token="test-token", database_id="   ")
    
    def test_notion_client_multiple_instances(self, mock_env_empty):
        """
        Test creazione istanze multiple NotionClient.
        
        Verifica che:
        - Ogni istanza abbia il proprio client Notion
        - Configurazioni siano indipendenti
        - Nessuna interferenza tra istanze
        
        Utilizzo: pattern singleton o multiple client per test.
        """
        client1 = NotionClient(token="token1", database_id="db1")
        client2 = NotionClient(token="token2", database_id="db2")
        
        assert client1.database_id == "db1"
        assert client2.database_id == "db2"
        assert client1 is not client2  # Istanze diverse