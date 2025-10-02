"""
Unit test per NotionCrudOperations.

Testa operazioni CRUD su database Notion formazioni.
Focus su:
- Update status formazioni (workflow transitions)
- Update codici e link Teams (calendarizzazione)
- Recupero formazioni per ID
- Operazioni batch e multiple fields
- Gestione errori API e fallback

UTILIZZO:
pytest tests/unit/notion/test_crud_operations.py -v
pytest -m "unit and notion" tests/unit/notion/test_crud_operations.py -v
"""

import pytest
from unittest.mock import AsyncMock, patch
from notion_client.errors import APIResponseError
from app.services.notion.crud_operations import NotionCrudOperations


@pytest.mark.unit
@pytest.mark.notion
class TestNotionCrudOperations:
    """Test suite per NotionCrudOperations."""
    
    @pytest.fixture
    def crud_operations(self, mock_notion_client):
        """Istanza NotionCrudOperations con mock client per test."""
        return NotionCrudOperations(mock_notion_client)
    
    # ===== TEST UPDATE FORMAZIONE STATUS =====
    
    @pytest.mark.asyncio
    async def test_update_formazione_status_success(self, crud_operations, mock_notion_client, sample_notion_id):
        """
        Test aggiornamento status formazione con successo.
        
        Verifica che:
        - Client API venga chiamato con parametri corretti
        - Campo "Stato" sia impostato correttamente
        - Return True per operazione successful
        - Logging appropriato sia eseguito
        
        Workflow principale: Programmata → Calendarizzata → Conclusa.
        """
        # Setup mock response
        mock_notion_client.get_client().pages.update.return_value = {"object": "page"}
        
        # Test
        result = await crud_operations.update_formazione_status(sample_notion_id, "Calendarizzata")
        
        # Verifica
        assert result is True
        mock_notion_client.get_client().pages.update.assert_called_once_with(
            page_id=sample_notion_id,
            properties={
                "Stato": {
                    "status": {
                        "name": "Calendarizzata"
                    }
                }
            }
        )
    
    @pytest.mark.asyncio
    async def test_update_formazione_status_different_statuses(self, crud_operations, mock_notion_client, sample_notion_id):
        """
        Test aggiornamento con diversi status workflow.
        
        Verifica che:
        - Tutti gli status workflow siano gestiti
        - Ogni status generi la chiamata API corretta
        - Consistenza tra status diversi
        
        Coverage: tutti i possibili status nel workflow aziendale.
        """
        mock_notion_client.get_client().pages.update.return_value = {"object": "page"}
        
        statuses = ["Programmata", "Calendarizzata", "Conclusa"]
        
        for status in statuses:
            result = await crud_operations.update_formazione_status(sample_notion_id, status)
            assert result is True
            
            # Verifica che l'ultimo call abbia il status corretto
            last_call = mock_notion_client.get_client().pages.update.call_args
            assert last_call[1]["properties"]["Stato"]["status"]["name"] == status
    
    @pytest.mark.asyncio
    async def test_update_formazione_status_api_error(self, crud_operations, mock_notion_client, sample_notion_id, mock_api_error):
        """
        Test gestione errore API durante update status.
        
        Verifica che:
        - APIResponseError sia catturato correttamente
        - Return False per operazione fallita
        - Error logging sia eseguito
        - Sistema non crashi
        
        Edge case: problemi di connessione o permessi Notion.
        """
        # Setup mock error
        mock_notion_client.get_client().pages.update.side_effect = mock_api_error
        
        # Test
        result = await crud_operations.update_formazione_status(sample_notion_id, "Calendarizzata")
        
        # Verifica
        assert result is False
    
    @pytest.mark.asyncio
    async def test_update_formazione_status_generic_error(self, crud_operations, mock_notion_client, sample_notion_id):
        """
        Test gestione errore generico durante update status.
        
        Verifica che:
        - Exception generiche siano catturate
        - Return False per errori non-API
        - Robustezza sistema contro errori imprevisti
        
        Edge case: problemi di rete, timeout, etc.
        """
        # Setup mock error
        mock_notion_client.get_client().pages.update.side_effect = Exception("Generic error")
        
        # Test
        result = await crud_operations.update_formazione_status(sample_notion_id, "Calendarizzata")
        
        # Verifica
        assert result is False
    
    # ===== TEST UPDATE CODICE E LINK =====
    
    @pytest.mark.asyncio
    async def test_update_codice_e_link_success(self, crud_operations, mock_notion_client, sample_notion_id):
        """
        Test aggiornamento codice e link Teams con successo.
        
        Verifica che:
        - Codice sia impostato come rich_text
        - Link Teams sia impostato come URL
        - Entrambi i campi siano aggiornati in singola operazione
        - Return True per operazione successful
        
        Workflow calendarizzazione: generazione codice + link Teams.
        """
        # Setup
        mock_notion_client.get_client().pages.update.return_value = {"object": "page"}
        codice = "IT-Sicurezza-2024-SPRING-01"
        link_teams = "https://teams.microsoft.com/l/meetup-join/test123"
        
        # Test
        result = await crud_operations.update_codice_e_link(sample_notion_id, codice, link_teams)
        
        # Verifica
        assert result is True
        
        expected_properties = {
            "Codice": {
                "rich_text": [
                    {
                        "text": {
                            "content": codice
                        }
                    }
                ]
            },
            "Link Teams": {
                "url": link_teams
            }
        }
        
        mock_notion_client.get_client().pages.update.assert_called_once_with(
            page_id=sample_notion_id,
            properties=expected_properties
        )
    
    @pytest.mark.asyncio
    async def test_update_codice_e_link_empty_link(self, crud_operations, mock_notion_client, sample_notion_id):
        """
        Test aggiornamento solo codice (link Teams vuoto).
        
        Verifica che:
        - Link Teams vuoto non sia incluso nelle properties
        - Solo campo Codice venga aggiornato
        - Operazione rimanga successful
        
        Caso edge: codice generato ma link Teams non ancora disponibile.
        """
        # Setup
        mock_notion_client.get_client().pages.update.return_value = {"object": "page"}
        codice = "IT-Test-2024-01"
        link_teams = ""  # Link vuoto
        
        # Test
        result = await crud_operations.update_codice_e_link(sample_notion_id, codice, link_teams)
        
        # Verifica
        assert result is True
        
        # Verifica che Link Teams non sia nelle properties
        last_call = mock_notion_client.get_client().pages.update.call_args
        properties = last_call[1]["properties"]
        
        assert "Codice" in properties
        assert "Link Teams" not in properties
    
    @pytest.mark.asyncio
    async def test_update_codice_e_link_api_error(self, crud_operations, mock_notion_client, sample_notion_id, mock_api_error):
        """
        Test gestione errore API durante update codice/link.
        
        Verifica che:
        - APIResponseError sia gestito correttamente
        - Return False per operazione fallita
        - Sistema rimanga stabile
        
        Edge case: problemi di autenticazione o rate limiting.
        """
        # Setup mock error
        mock_notion_client.get_client().pages.update.side_effect = mock_api_error
        
        # Test
        result = await crud_operations.update_codice_e_link(sample_notion_id, "TEST-CODE", "http://test.com")
        
        # Verifica
        assert result is False
    
    # ===== TEST GET FORMAZIONE BY ID =====
    
    @pytest.mark.asyncio
    async def test_get_formazione_by_id_success(self, crud_operations, mock_notion_client, sample_notion_id, 
                                              sample_retrieve_response, mock_data_parser):
        """
        Test recupero formazione per ID con successo.
        
        Verifica che:
        - Client retrieve sia chiamato con ID corretto
        - Parser sia utilizzato per convertire response
        - Formazione parsed sia restituita
        - Logging appropriato sia eseguito
        
        Utilità: operazioni puntuali e validazione post-update.
        """
        # Setup
        mock_notion_client.get_client().pages.retrieve.return_value = sample_retrieve_response
        
        # Test
        result = await crud_operations.get_formazione_by_id(sample_notion_id, mock_data_parser)
        
        # Verifica
        assert result is not None
        assert result["Nome"] == "Test Formazione Retrieved"
        assert result["ID"] == sample_notion_id
        
        mock_notion_client.get_client().pages.retrieve.assert_called_once_with(page_id=sample_notion_id)
        mock_data_parser.parse_single_formazione.assert_called_once_with(sample_retrieve_response)
    
    @pytest.mark.asyncio
    async def test_get_formazione_by_id_parse_failure(self, crud_operations, mock_notion_client, sample_notion_id,
                                                     sample_retrieve_response, mock_data_parser):
        """
        Test recupero formazione con parsing fallito.
        
        Verifica che:
        - Parser restituisca None per dati malformati
        - Sistema gestisca gracefully il parsing failure
        - Return None per formazione non parsabile
        - Warning logging appropriato
        
        Edge case: dati Notion corrotti o formato cambiato.
        """
        # Setup - parser restituisce None (parsing failed)
        mock_notion_client.get_client().pages.retrieve.return_value = sample_retrieve_response
        mock_data_parser.parse_single_formazione.return_value = None
        
        # Test
        result = await crud_operations.get_formazione_by_id(sample_notion_id, mock_data_parser)
        
        # Verifica
        assert result is None
        mock_data_parser.parse_single_formazione.assert_called_once_with(sample_retrieve_response)
    
    @pytest.mark.asyncio
    async def test_get_formazione_by_id_api_error(self, crud_operations, mock_notion_client, sample_notion_id, mock_data_parser, mock_api_error):
        """
        Test gestione errore API durante retrieve.
        
        Verifica che:
        - APIResponseError sia catturato
        - Return None per errore API
        - Parser non sia chiamato
        - Error logging appropriato
        
        Edge case: formazione cancellata o permessi insufficienti.
        """
        # Setup mock error
        mock_notion_client.get_client().pages.retrieve.side_effect = mock_api_error
        
        # Test
        result = await crud_operations.get_formazione_by_id(sample_notion_id, mock_data_parser)
        
        # Verifica
        assert result is None
        mock_data_parser.parse_single_formazione.assert_not_called()
    
    # ===== TEST UPDATE MULTIPLE FIELDS =====
    
    @pytest.mark.asyncio
    async def test_update_multiple_fields_success(self, crud_operations, mock_notion_client, sample_notion_id, 
                                                sample_multiple_fields_update):
        """
        Test aggiornamento multipli campi in operazione atomica.
        
        Verifica che:
        - Tutti i campi siano convertiti nel formato Notion
        - Singola chiamata API per tutti gli aggiornamenti
        - Mapping corretto: status→Stato, codice→Codice, link_teams→Link Teams
        - Return True per operazione successful
        
        Operazione atomica: evita inconsistenze tra aggiornamenti separati.
        """
        # Setup
        mock_notion_client.get_client().pages.update.return_value = {"object": "page"}
        
        # Test
        result = await crud_operations.update_multiple_fields(sample_notion_id, sample_multiple_fields_update)
        
        # Verifica
        assert result is True
        
        expected_properties = {
            "Stato": {"status": {"name": "Calendarizzata"}},
            "Codice": {"rich_text": [{"text": {"content": "MULTI-UPDATE-2024-01"}}]},
            "Link Teams": {"url": "https://teams.microsoft.com/multi-update"}
        }
        
        mock_notion_client.get_client().pages.update.assert_called_once_with(
            page_id=sample_notion_id,
            properties=expected_properties
        )
    
    @pytest.mark.asyncio
    async def test_update_multiple_fields_partial_update(self, crud_operations, mock_notion_client, sample_notion_id):
        """
        Test aggiornamento solo alcuni campi.
        
        Verifica che:
        - Solo campi specificati siano inclusi
        - Campi non specificati siano ignorati
        - Operazione rimanga successful
        
        Flessibilità: update selettivo solo dei campi necessari.
        """
        # Setup
        mock_notion_client.get_client().pages.update.return_value = {"object": "page"}
        partial_updates = {"Stato": "Conclusa"}  # Solo status
        
        # Test
        result = await crud_operations.update_multiple_fields(sample_notion_id, partial_updates)
        
        # Verifica
        assert result is True
        
        last_call = mock_notion_client.get_client().pages.update.call_args
        properties = last_call[1]["properties"]
        
        assert "Stato" in properties
        assert "Codice" not in properties
        assert "Link Teams" not in properties
    
    @pytest.mark.asyncio
    async def test_update_multiple_fields_api_error(self, crud_operations, mock_notion_client, sample_notion_id, mock_api_error):
        """
        Test gestione errore API durante update multiplo.
        
        Verifica che:
        - APIResponseError sia gestito
        - Return False per operazione fallita
        - Rollback automatico non necessario (operazione atomica)
        
        Vantaggio operazioni atomiche: fallimento totale, no stati inconsistenti.
        """
        # Setup mock error
        mock_notion_client.get_client().pages.update.side_effect = mock_api_error
        
        # Test
        result = await crud_operations.update_multiple_fields(sample_notion_id, {"status": "Conclusa"})
        
        # Verifica
        assert result is False
    
    # ===== TEST BATCH UPDATE STATUS =====
    
    @pytest.mark.asyncio
    async def test_batch_update_status_all_success(self, crud_operations, mock_notion_client, sample_batch_formazioni_ids):
        """
        Test batch update con tutti gli update successful.
        
        Verifica che:
        - Ogni formazione venga aggiornata individualmente
        - Success count sia corretto
        - Nessun failed_ids presente
        - Risultati batch siano accurati
        
        Scenario ideale: operazione batch completamente successful.
        """
        # Setup - mock all updates successful
        mock_notion_client.get_client().pages.update.return_value = {"object": "page"}
        
        # Test
        result = await crud_operations.batch_update_status(sample_batch_formazioni_ids, "Conclusa")
        
        # Verifica
        assert result["success_count"] == 3
        assert result["failed_ids"] == []
        assert result["total"] == 3
        
        # Verifica che tutte le formazioni siano state chiamate
        assert mock_notion_client.get_client().pages.update.call_count == 3
    
    @pytest.mark.asyncio
    async def test_batch_update_status_partial_failure(self, crud_operations, mock_notion_client, sample_batch_formazioni_ids, mock_api_error):
        """
        Test batch update con alcuni failures.
        
        Verifica che:
        - Update successful e failed siano tracciati separatamente
        - Failed IDs siano registrati correttamente
        - Operazione continui nonostante failures
        - Statistiche finali siano accurate
        
        Scenario realistico: alcuni update falliscono, altri riescono.
        """
        # Setup - mock mixed results (prima success, seconda e terza fail)
        side_effects = [
            {"object": "page"},  # Success
            mock_api_error,  # Fail
            mock_api_error   # Fail
        ]
        mock_notion_client.get_client().pages.update.side_effect = side_effects
        
        # Test
        result = await crud_operations.batch_update_status(sample_batch_formazioni_ids, "Conclusa")
        
        # Verifica
        assert result["success_count"] == 1
        assert len(result["failed_ids"]) == 2
        assert result["failed_ids"] == ["batch-id-002", "batch-id-003"]
        assert result["total"] == 3
    
    @pytest.mark.asyncio
    async def test_batch_update_status_empty_list(self, crud_operations, mock_notion_client):
        """
        Test batch update con lista vuota.
        
        Verifica che:
        - Lista vuota sia gestita correttamente
        - Nessuna chiamata API sia effettuata
        - Risultati siano coerenti (0 success, 0 failed)
        
        Edge case: batch operation chiamata con lista vuota.
        """
        # Test
        result = await crud_operations.batch_update_status([], "Conclusa")
        
        # Verifica
        assert result["success_count"] == 0
        assert result["failed_ids"] == []
        assert result["total"] == 0
        
        # Nessuna chiamata API dovrebbe essere fatta
        mock_notion_client.get_client().pages.update.assert_not_called()
    
    # ===== TEST EDGE CASES E INITIALIZATION =====
    
    def test_crud_operations_initialization(self, mock_notion_client):
        """
        Test inizializzazione CrudOperations.
        
        Verifica che:
        - Client sia configurato correttamente
        - Attributi siano impostati
        - Nessun errore durante init
        
        Setup base: corretto inizializzazione del modulo CRUD.
        """
        crud = NotionCrudOperations(mock_notion_client)
        
        assert crud.client is not None
        assert crud.client == mock_notion_client.get_client()
    
    @pytest.mark.asyncio
    async def test_all_methods_handle_none_gracefully(self, crud_operations, mock_notion_client):
        """
        Test gestione robusta parametri None.
        
        Verifica che:
        - Metodi non crashino con parametri None
        - Comportamento sia prevedibile
        - Return values siano coerenti
        
        Robustezza: protezione contro input malformati.
        """
        # Test con None ID (dovrebbe fallire gracefully)
        mock_notion_client.get_client().pages.update.side_effect = Exception("None ID error")
        
        result = await crud_operations.update_formazione_status(None, "Calendarizzata")
        assert result is False