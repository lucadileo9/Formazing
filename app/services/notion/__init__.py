"""
NotionService - Facade unificata per moduli Notion

Questo modulo espone:
- API pubblica unificata (backward compatible)
- Orchestrazione moduli specializzati
- Error handling centralizzato
- Interface semplificata per il resto del sistema

ARCHITETTURA MODULARE:
- NotionClient: Connessione e autenticazione
- NotionQueryBuilder: Costruzione query
- NotionDataParser: Parsing e mapping dati
- NotionCrudOperations: Operazioni database
- NotionDiagnostics: Monitoring e debug
"""

import logging
from typing import List, Dict, Optional

from .notion_client import NotionClient, NotionClientError
from .query_builder import NotionQueryBuilder
from .data_parser import NotionDataParser
from .crud_operations import NotionCrudOperations
from .diagnostics import NotionDiagnostics


logger = logging.getLogger(__name__)


class NotionService:
    """
    Facade unificata per tutti i servizi Notion.
    
    BACKWARD COMPATIBILITY: Mantiene stessa API del monolite precedente.
    
    RESPONSABILITÀ:
    - Orchestrazione moduli specializzati
    - API pubblica semplificata
    - Error handling centralizzato
    - Delegation pattern per operazioni specifiche
    """
    
    def __init__(self, token: str = None, database_id: str = None):
        """
        Inizializza NotionService con architettura modulare.
        
        Args:
            token: Token Notion (da .env se None)
            database_id: ID database formazioni (da .env se None)
        """
        try:
            # Inizializzazione moduli in ordine di dipendenza
            self.client = NotionClient(token, database_id)
            self.query_builder = NotionQueryBuilder()
            self.data_parser = NotionDataParser()
            self.crud_operations = NotionCrudOperations(self.client)
            self.diagnostics = NotionDiagnostics(self.client)
            
            logger.info("NotionService modulare inizializzato con successo")
            
        except Exception as e:
            logger.error(f"Errore inizializzazione NotionService: {e}")
            raise NotionServiceError(f"Inizializzazione fallita: {e}")
    
    # ===============================
    # API PUBBLICA - BACKWARD COMPATIBLE
    # ===============================
    
    async def get_formazioni_by_status(self, status: str) -> List[Dict]:
        """
        Recupera formazioni filtrate per status specifico.
        
        METODO PRINCIPALE - Stesso API del monolite precedente.
        
        Args:
            status: Status formazione ("Programmata", "Calendarizzata", "Conclusa")
            
        Returns:
            List[Dict]: Lista formazioni filtrate e normalizzate
            
        Raises:
            NotionServiceError: Errori API o parsing dati
        """
        logger.info(f"Recupero formazioni con status: '{status}'")
        
        try:
            # 1. Costruisci query con QueryBuilder
            query = self.query_builder.build_status_filter_query(
                status=status,
                database_id=self.client.get_database_id()
            )
            
            # 2. Esegui query con Client
            response = self.client.get_client().databases.query(**query)
            
            # 3. Parsa risultati con DataParser
            formazioni = self.data_parser.parse_formazioni_list(response)
            
            logger.info(f"Recuperate {len(formazioni)} formazioni con status '{status}'")
            return formazioni
            
        except Exception as e:
            logger.error(f"Errore recupero formazioni '{status}': {e}")
            raise NotionServiceError(f"Errore recupero formazioni: {e}")
    
    async def update_formazione_status(self, notion_id: str, new_status: str) -> bool:
        """
        Aggiorna status di una formazione specifica.
        
        Delega a CrudOperations.
        """
        return await self.crud_operations.update_formazione_status(notion_id, new_status)
    
    async def update_codice_e_link(self, notion_id: str, codice: str, link_teams: str) -> bool:
        """
        Aggiorna codice formazione e link Teams.
        
        Delega a CrudOperations.
        """
        return await self.crud_operations.update_codice_e_link(notion_id, codice, link_teams)
    
    async def get_formazione_by_id(self, notion_id: str) -> Optional[Dict]:
        """
        Recupera formazione specifica per ID Notion.
        
        Delega a CrudOperations.
        """
        return await self.crud_operations.get_formazione_by_id(notion_id, self.data_parser)
    
    async def test_connection(self) -> Dict:
        """
        Testa connessione API Notion e configurazione database.
        
        Delega a Diagnostics.
        """
        return await self.diagnostics.test_connection()
    
    def get_service_stats(self) -> Dict:
        """
        Statistiche interne servizio per monitoring.
        
        Delega a Diagnostics.
        """
        return self.diagnostics.get_service_stats()
    
    # ===============================
    # API ESTESE - NUOVE FUNZIONALITÀ
    # ===============================
    
    async def get_formazioni_by_area(self, area: str) -> List[Dict]:
        """
        Recupera formazioni filtrate per area aziendale.
        
        NUOVA FUNZIONALITÀ abilitata dall'architettura modulare.
        """
        logger.info(f"Recupero formazioni per area: '{area}'")
        
        try:
            query = self.query_builder.build_area_filter_query(
                area=area,
                database_id=self.client.get_database_id()
            )
            
            response = self.client.get_client().databases.query(**query)
            formazioni = self.data_parser.parse_formazioni_list(response)
            
            logger.info(f"Recuperate {len(formazioni)} formazioni per area '{area}'")
            return formazioni
            
        except Exception as e:
            logger.error(f"Errore recupero formazioni area '{area}': {e}")
            raise NotionServiceError(f"Errore recupero per area: {e}")
    
    async def get_formazioni_by_status_and_area(self, status: str, area: str) -> List[Dict]:
        """
        Recupera formazioni con filtri combinati.
        
        NUOVA FUNZIONALITÀ per query complesse.
        """
        logger.info(f"Recupero formazioni: status='{status}', area='{area}'")
        
        try:
            query = self.query_builder.build_combined_filter_query(
                status=status,
                area=area,
                database_id=self.client.get_database_id()
            )
            
            response = self.client.get_client().databases.query(**query)
            formazioni = self.data_parser.parse_formazioni_list(response)
            
            logger.info(f"Recuperate {len(formazioni)} formazioni con filtri combinati")
            return formazioni
            
        except Exception as e:
            logger.error(f"Errore recupero formazioni combinate: {e}")
            raise NotionServiceError(f"Errore recupero combinato: {e}")
    
    async def validate_database_structure(self) -> Dict:
        """
        Valida struttura database per compatibilità.
        
        NUOVA FUNZIONALITÀ per setup e manutenzione.
        """
        return await self.diagnostics.validate_database_structure()
    
    async def batch_update_status(self, formazioni_ids: List[str], new_status: str) -> Dict:
        """
        Aggiorna status per batch di formazioni.
        
        NUOVA FUNZIONALITÀ per operazioni bulk.
        """
        return await self.crud_operations.batch_update_status(formazioni_ids, new_status)


class NotionServiceError(Exception):
    """Eccezione specifica per errori NotionService."""
    pass


# Export pubblici per backward compatibility
__all__ = [
    'NotionService',
    'NotionServiceError'
]