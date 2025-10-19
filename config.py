"""
Configurazione centralizzata Formazing App

Gestisce caricamento variabili ambiente e configurazioni globali
per tutti i servizi (Telegram, Notion, Microsoft Graph, Flask).
"""

import os
from dotenv import load_dotenv


# Carica automaticamente variabili da .env
load_dotenv()


class Config:
    """Configurazione base application."""
    
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    
    # ===== FLASK CONFIG =====
    SECRET_KEY = os.getenv('FLASK_SECRET_KEY', 'dev-secret-key-change-in-production')
    BASIC_AUTH_USERNAME = os.getenv('FLASK_BASIC_AUTH_USERNAME', 'admin')
    BASIC_AUTH_PASSWORD = os.getenv('FLASK_BASIC_AUTH_PASSWORD')
    FLASK_PORT = int(os.getenv('FLASK_PORT', 5000))
    DEBUG = os.getenv('DEBUG_MODE', 'False').lower() == 'true'
    
    # ===== TELEGRAM CONFIG =====
    TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
    TELEGRAM_GROUPS_CONFIG = 'config/telegram_groups.json'
    TELEGRAM_TEMPLATES_CONFIG = 'config/message_templates.yaml'
    
    # ===== NOTION CONFIG =====
    NOTION_TOKEN = os.getenv('NOTION_TOKEN')
    NOTION_DATABASE_ID = os.getenv('NOTION_DATABASE_ID')
    
    # ===== MICROSOFT GRAPH CONFIG =====
    MICROSOFT_CLIENT_ID = os.getenv('MICROSOFT_CLIENT_ID')
    MICROSOFT_CLIENT_SECRET = os.getenv('MICROSOFT_CLIENT_SECRET') 
    MICROSOFT_TENANT_ID = os.getenv('MICROSOFT_TENANT_ID')
    MICROSOFT_USER_EMAIL = os.getenv('MICROSOFT_USER_EMAIL')  # Organizzatore eventi (es. lucadileo@jemore.it)
    
    # ===== LOGGING CONFIG =====
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO').upper()
    
    @classmethod
    def validate_config(cls) -> dict:
        """
        Valida configurazione critica per startup.
        
        Returns:
            dict: Risultati validazione per ogni servizio
        """
        validation = {
            'telegram': bool(cls.TELEGRAM_BOT_TOKEN),
            'notion': bool(cls.NOTION_TOKEN and cls.NOTION_DATABASE_ID),
            'microsoft_graph': bool(
                cls.MICROSOFT_CLIENT_ID and 
                cls.MICROSOFT_CLIENT_SECRET and 
                cls.MICROSOFT_TENANT_ID and
                cls.MICROSOFT_USER_EMAIL
            ),
            'flask_auth': bool(cls.BASIC_AUTH_PASSWORD),
            'overall_ok': False
        }
        
        # Almeno Telegram e Notion devono essere configurati
        # Microsoft Graph è opzionale ma consigliato
        validation['overall_ok'] = validation['telegram'] and validation['notion']
        
        return validation