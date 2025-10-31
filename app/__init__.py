#!/usr/bin/env python3
"""
🏗️ Factory Flask App per Formazing

Configurazione centralizzata dell'applicazione Flask con:
- Basic Authentication per sicurezza
- Template engine Jinja2 
- Static files (CSS, JS, images)
- Error handling centralizzato
- Logging configurato
"""

from flask import Flask
from flask_httpauth import HTTPBasicAuth
from config import Config
import logging

# Inizializza l'autenticazione Basic HTTP
auth = HTTPBasicAuth()

# Logger per app factory
logger = logging.getLogger(__name__)

def create_app():
    """
    Factory pattern per creare l'applicazione Flask.
    
    Returns:
        Flask: Applicazione configurata e pronta
    """
    # Crea l'app Flask
    app = Flask(__name__)
    
    # Carica configurazione
    app.config.from_object(Config)
    
    # Configura logging centralizzato
    log_level = app.config.get('LOG_LEVEL', 'INFO').upper()
    log_file = app.config.get('LOG_FILE', 'app.log')
    log_format = app.config.get('LOG_FORMAT', '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    # Rimuovi eventuali handler pre-esistenti per evitare duplicati
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)
        
    # Configura handler per file
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(logging.Formatter(log_format))
    
    # Configura handler per console
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(logging.Formatter(log_format))
    
    # Aggiungi handler al root logger
    logging.root.addHandler(file_handler)
    logging.root.addHandler(stream_handler)
    logging.root.setLevel(log_level)
    
    # Registra il sistema di autenticazione
    @auth.verify_password
    def verify_password(username, password):
        """Verifica credenziali Basic Auth."""
        return (username == Config.BASIC_AUTH_USERNAME and 
                password == Config.BASIC_AUTH_PASSWORD)
    
    # Registra le routes
    from app.routes import main
    app.register_blueprint(main)
    
    # 🎯 Inizializza TrainingService Singleton all'avvio
    # Questo garantisce che il bot Telegram sia online PRIMA di gestire richieste
    logger.info("🎯 Inizializzazione TrainingService Singleton...")
    from app.services.training_service import TrainingService
    training_service = TrainingService.get_instance()
    logger.info("✅ TrainingService pronto (bot Telegram avviato se processo principale)")
    
    # ✨ Filtri Jinja2 personalizzati
    @app.template_filter('format_area')
    def format_area_filter(area):
        """
        Formatta campo Area per visualizzazione in template.
        
        Gestisce sia liste che stringhe:
        - ['IT', 'R&D'] → 'IT, R&D'
        - ['IT'] → 'IT'
        - 'IT' → 'IT'
        - [] → 'N/A'
        """
        if isinstance(area, list):
            return ', '.join(area) if area else 'N/A'
        elif isinstance(area, str):
            return area if area else 'N/A'
        else:
            return 'N/A'
    
    # Error handlers
    @app.errorhandler(404)
    def not_found_error(error):
        return {'error': 'Risorsa non trovata'}, 404
    
    @app.errorhandler(500) 
    def internal_error(error):
        return {'error': 'Errore interno del server'}, 500
    
    return app