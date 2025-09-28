"""
Mock NotionService per testing

Questo è l'UNICO componente mockato nel sistema di test.
Fornisce dati realistici e controllati per testare tutti gli altri componenti reali.

CARATTERISTICHE:
- Dati dinamici basati su data corrente
- Formazioni distribuite su oggi/domani/settimana
- Edge cases per testing robusto
- Sempre consistente per test ripetibili
"""

from datetime import datetime, timedelta
from typing import List, Dict, Optional


class MockNotionService:
    """
    Mock realistico del NotionService.
    
    Genera dati di test dinamici che simulano:
    - Formazioni calendarizzate per diversi giorni
    - Diverse aree aziendali
    - Vari formati di data/ora
    - Edge cases (link mancanti, date malformate)
    """
    
    def __init__(self):
        """Inizializza con base date corrente per dati dinamici."""
        self.base_date = datetime.now()
        
    async def get_formazioni_by_status(self, status: str) -> List[Dict]:
        """
        Restituisce formazioni mock filtrate per status.
        
        Args:
            status: "Calendarizzata", "Completata", etc.
            
        Returns:
            Lista formazioni mock realistiche
        """
        if status == 'Calendarizzata':
            return self._get_mock_formazioni_calendarizzate()
        elif status == 'Completata':
            return self._get_mock_formazioni_completate()
        else:
            return []
    
    def _get_mock_formazioni_calendarizzate(self) -> List[Dict]:
        """
        Genera formazioni calendarizzate per testing comandi.
        
        DISTRIBUZIONE:
        - 2 formazioni OGGI (per /oggi)
        - 1 formazione DOMANI (per /domani)  
        - 3 formazioni nel resto della settimana (per /settimana)
        - 1 edge case con data ISO
        - 1 edge case senza link Teams
        """
        today = self.base_date
        
        return [
            # === FORMAZIONI OGGI ===
            {
                'Nome': 'Python Fundamentals Workshop',
                'Area': 'IT',
                'Data/Ora': today.strftime('%d/%m/%Y 09:00'),
                'Codice': 'PY001',
                'Link Teams': 'https://teams.microsoft.com/l/meetup-join/py001',
                'Stato/Fase': 'Calendarizzata',
                'Docente': 'Marco Rossi',
                'Descrizione': 'Corso base Python per sviluppatori'
            },
            {
                'Nome': 'Advanced Git Workflows',
                'Area': 'IT', 
                'Data/Ora': today.strftime('%d/%m/%Y 14:30'),
                'Codice': 'GIT001',
                'Link Teams': 'https://teams.microsoft.com/l/meetup-join/git001',
                'Stato/Fase': 'Calendarizzata',
                'Docente': 'Laura Bianchi',
                'Descrizione': 'Tecniche avanzate di version control'
            },
            
            # === FORMAZIONI DOMANI ===
            {
                'Nome': 'Leadership & Team Management',
                'Area': 'HR',
                'Data/Ora': (today + timedelta(days=1)).strftime('%d/%m/%Y 10:00'),
                'Codice': 'HR001',
                'Link Teams': 'https://teams.microsoft.com/l/meetup-join/hr001',
                'Stato/Fase': 'Calendarizzata',
                'Docente': 'Giuseppe Verde',
                'Descrizione': 'Tecniche di leadership moderna'
            },
            
            # === FORMAZIONI SETTIMANA ===
            {
                'Nome': 'Digital Marketing Analytics',
                'Area': 'Marketing',
                'Data/Ora': (today + timedelta(days=2)).strftime('%d/%m/%Y 15:00'),
                'Codice': 'MKT001',
                'Link Teams': 'https://teams.microsoft.com/l/meetup-join/mkt001',
                'Stato/Fase': 'Calendarizzata',
                'Docente': 'Francesca Neri',
                'Descrizione': 'Analisi dei dati di marketing digitale'
            },
            {
                'Nome': 'Legal Compliance & GDPR',
                'Area': 'Legale',
                'Data/Ora': (today + timedelta(days=3)).strftime('%d/%m/%Y 11:30'),
                'Codice': 'LEG001',
                'Link Teams': 'https://teams.microsoft.com/l/meetup-join/leg001',
                'Stato/Fase': 'Calendarizzata',
                'Docente': 'Avv. Paolo Grigio',
                'Descrizione': 'Aggiornamenti normativi e compliance'
            },
            {
                'Nome': 'Innovation Workshop R&D',
                'Area': 'R&D',
                'Data/Ora': (today + timedelta(days=4)).strftime('%d/%m/%Y 16:00'),
                'Codice': 'RD001',
                'Link Teams': 'https://teams.microsoft.com/l/meetup-join/rd001',
                'Stato/Fase': 'Calendarizzata',
                'Docente': 'Dr. Maria Blu',
                'Descrizione': 'Metodologie innovative per la ricerca'
            },
            
            # === EDGE CASES per testing robusto ===
            {
                'Nome': 'Test Formazione Senza Link',
                'Area': 'R&D',
                'Data/Ora': (today + timedelta(days=5)).strftime('%d/%m/%Y 12:00'),
                'Codice': 'EDGE001',
                'Link Teams': '',  # Link vuoto per testare gestione errori
                'Stato/Fase': 'Calendarizzata',
                'Docente': 'Test Docente',
                'Descrizione': 'Formazione di test senza link Teams'
            },
            {
                'Nome': 'Test Formato Data ISO',
                'Area': 'IT',
                'Data/Ora': (today + timedelta(days=6)).isoformat() + 'Z',  # Formato ISO
                'Codice': 'ISO001',
                'Link Teams': 'https://teams.microsoft.com/l/meetup-join/iso001',
                'Stato/Fase': 'Calendarizzata',
                'Docente': 'ISO Tester',
                'Descrizione': 'Test parsing formato data ISO'
            }
        ]
    
    def _get_mock_formazioni_completate(self) -> List[Dict]:
        """
        Formazioni completate per test feedback.
        
        Simulate formazioni recentemente completate per testare
        l'invio di richieste feedback.
        """
        yesterday = self.base_date - timedelta(days=1)
        last_week = self.base_date - timedelta(days=7)
        
        return [
            {
                'Nome': 'Python Course Completato',
                'Area': 'IT',
                'Data/Ora': yesterday.strftime('%d/%m/%Y 09:00'),
                'Codice': 'COMP001',
                'Link Teams': 'https://teams.microsoft.com/l/meetup-join/comp001',
                'Stato/Fase': 'Completata',
                'Docente': 'Formatore Test',
                'Descrizione': 'Corso Python completato ieri'
            },
            {
                'Nome': 'HR Workshop Settimana Scorsa',
                'Area': 'HR',
                'Data/Ora': last_week.strftime('%d/%m/%Y 14:30'),
                'Codice': 'COMP002',
                'Link Teams': 'https://teams.microsoft.com/l/meetup-join/comp002',
                'Stato/Fase': 'Completata',
                'Docente': 'HR Trainer',
                'Descrizione': 'Workshop HR completato la settimana scorsa'
            }
        ]
    
    def get_current_test_info(self) -> Dict:
        """
        Utility per debug - informazioni sui dati mock generati.
        
        Returns:
            Dizionario con statistiche dati mock
        """
        calendarizzate = len(self._get_mock_formazioni_calendarizzate())
        completate = len(self._get_mock_formazioni_completate())
        
        return {
            'base_date': self.base_date.strftime('%d/%m/%Y %H:%M'),
            'formazioni_calendarizzate': calendarizzate,
            'formazioni_completate': completate,
            'today_formazioni': 2,  # Sempre 2 per oggi
            'tomorrow_formazioni': 1,  # Sempre 1 per domani
            'week_formazioni': calendarizzate,  # Tutte le calendarizzate
            'edge_cases': 2  # Senza link + formato ISO
        }