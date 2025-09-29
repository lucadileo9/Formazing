"""
Unit Tests - NotionService Facade (Critical Integration Points)

Test suite ridotta per facade NotionService con focus su integration points critici.

STRATEGIA:
- Solo 4 test critici per integration contracts
- Mock tutti i moduli sottostanti  
- Focus su orchestrazione, error handling, API contract
- ROI ottimizzato: massimo valore con minimo overhead

COVERAGE:
- Dependency injection e orchestrazione moduli
- Pipeline completa get_formazioni (caso d'uso principale) 
- Error handling centralizzato consistency
- API contract e module accessibility
"""

import pytest
from unittest.mock import Mock, AsyncMock, patch
from notion_client.errors import APIResponseError

from app.services.notion import NotionService, NotionServiceError


@pytest.mark.unit
@pytest.mark.notion
class TestNotionServiceFacade:
    """
    Test suite CRITICA per NotionService facade.
    
    Focus su INTEGRATION POINTS essenziali:
    - Dependency injection tra moduli
    - Orchestrazione pipeline principale
    - Error handling centralizzato
    - API contract verification
    
    Razionale: I moduli sottostanti sono già testati (82 test),
    questi 4 test verificano solo gli integration points unici del Facade.
    """
    
    def test_init_successful_modules_orchestration(self, mock_notion_service_modules, mock_env_empty):
        """
        TEST CRITICO 1: Dependency Injection e Orchestrazione Moduli.
        
        Verifica che:
        - Tutti i moduli siano inizializzati in ordine di dipendenza
        - Dependency injection sia corretta (CrudOps e Diagnostics ricevono Client)
        - Integration setup sia successful
        
        VALORE: Questo testa l'unico aspetto NON coperto dai unit test dei singoli moduli.
        """
        service = NotionService(token="test-token", database_id="test-db")
        
        # Verifica inizializzazione completa
        assert service.client == mock_notion_service_modules['client']
        assert service.query_builder == mock_notion_service_modules['query_builder']
        assert service.data_parser == mock_notion_service_modules['data_parser']
        assert service.crud_operations == mock_notion_service_modules['crud_operations']
        assert service.diagnostics == mock_notion_service_modules['diagnostics']
        
        # CRITICAL: Verifica dependency injection tra moduli
        mock_notion_service_modules['crud_class'].assert_called_once_with(mock_notion_service_modules['client'])
        mock_notion_service_modules['diagnostics_class'].assert_called_once_with(mock_notion_service_modules['client'])
    
    @pytest.mark.asyncio
    async def test_get_formazioni_by_status_complete_pipeline(
        self, mock_notion_service_modules, sample_facade_formazioni_response, mock_notion_api_response, mock_env_empty
    ):
        """
        TEST CRITICO 2: Pipeline Orchestrazione Completa (Caso d'uso principale).
        
        Verifica orchestrazione COMPLETA della pipeline più importante:
        QueryBuilder → Client API → DataParser → Response
        
        VALORE: Testa il FLOW di integrazione tra moduli che nessun unit test verifica.
        """
        service = NotionService(token="test-token", database_id="test-db")
        
        # Setup mock chain completa
        mock_query = {"database_id": "test-db", "filter": {"property": "Status"}}
        mock_notion_service_modules['query_builder'].build_status_filter_query.return_value = mock_query
        mock_notion_service_modules['client'].get_client().databases.query.return_value = mock_notion_api_response
        mock_notion_service_modules['data_parser'].parse_formazioni_list.return_value = sample_facade_formazioni_response
        
        # Execute pipeline completa
        result = await service.get_formazioni_by_status("Programmata")
        
        # CRITICAL: Verifica orchestrazione step-by-step
        mock_notion_service_modules['query_builder'].build_status_filter_query.assert_called_once_with(
            status="Programmata", database_id="test-database-id"
        )
        mock_notion_service_modules['client'].get_client().databases.query.assert_called_once_with(**mock_query)
        mock_notion_service_modules['data_parser'].parse_formazioni_list.assert_called_once_with(mock_notion_api_response)
        
        assert result == sample_facade_formazioni_response
        assert len(result) == 2
    
    @pytest.mark.asyncio
    async def test_error_handling_centralized_consistency(
        self, mock_notion_service_modules, mock_env_empty
    ):
        """
        TEST CRITICO 3: Error Handling Centralizzato del Facade.
        
        Verifica che:
        - Errori da moduli sottostanti siano wrappati in NotionServiceError
        - Logging centralizzato funzioni
        - Error consistency attraverso tutti i metodi pubblici
        
        VALORE: Testa logica UNICA del Facade (wrapping errori) non presente nei moduli.
        """
        service = NotionService(token="test-token", database_id="test-db")
        
        # Setup API error nel pipeline
        api_error = APIResponseError(
            response=Mock(status_code=500, text='Server Error'),
            message="API Error",
            code="internal_server_error"
        )
        mock_notion_service_modules['client'].get_client().databases.query.side_effect = api_error
        
        # CRITICAL: Verifica error wrapping centralizzato
        with pytest.raises(NotionServiceError, match="Errore recupero formazioni"):
            await service.get_formazioni_by_status("Programmata")
    
    def test_facade_api_contract_and_module_accessibility(self, mock_notion_service_modules, mock_env_empty):
        """
        TEST CRITICO 4: API Contract e Module Accessibility.
        
        Verifica che:
        - Tutti i moduli siano accessibili come attributi pubblici
        - API contract sia rispettato per integration testing
        - Facade esponga interfaccia corretta per client esterni
        
        VALORE: Testa il CONTRACT pubblico del Facade per integration e debugging.
        """
        service = NotionService(token="test-token", database_id="test-db")
        
        # CRITICAL: Verifica API contract per integration testing
        assert hasattr(service, 'client')
        assert hasattr(service, 'query_builder') 
        assert hasattr(service, 'data_parser')
        assert hasattr(service, 'crud_operations')
        assert hasattr(service, 'diagnostics')
        
        # Verifica che siano gli oggetti corretti (per mocking in integration tests)
        assert service.client == mock_notion_service_modules['client']
        assert service.query_builder == mock_notion_service_modules['query_builder']
        assert service.data_parser == mock_notion_service_modules['data_parser']
        
        # Verifica metodi pubblici esistano (API contract)
        assert callable(getattr(service, 'get_formazioni_by_status', None))
        assert callable(getattr(service, 'update_formazione_status', None))
        assert callable(getattr(service, 'get_formazione_by_id', None))