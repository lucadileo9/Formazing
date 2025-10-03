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
    
    # Configura logging
    if not app.debug:
        logging.basicConfig(level=logging.INFO)
    
    # Registra il sistema di autenticazione
    @auth.verify_password
    def verify_password(username, password):
        """Verifica credenziali Basic Auth."""
        return (username == Config.BASIC_AUTH_USERNAME and 
                password == Config.BASIC_AUTH_PASSWORD)
    
    # Registra le routes
    from app.routes import main
    app.register_blueprint(main)
    
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