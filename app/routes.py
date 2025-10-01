#!/usr/bin/env python3
"""
🌐 Routes Flask per Formazing

Gestisce tutte le pagine web dell'applicazione:
- Homepage con login
- Dashboard formazioni  
- API endpoints per operazioni
- Pagine di gestione e preview
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from app import auth
from app.services.notion import NotionService, NotionServiceError
from config import Config
import logging
import traceback
import asyncio

# Configura logging con più dettagli
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),  # Console
        logging.FileHandler('app.log')  # File
    ]
)

logger = logging.getLogger(__name__)

# Blueprint principale per le routes
main = Blueprint('main', __name__)


@main.route('/')
def home():
    """
    Homepage con form di login.
    Se già autenticato, redirect alla dashboard.
    """
    return render_template('pages/login.html', 
                         title='Formazing - Gestione Formazioni',
                         app_name='Formazing')


@main.route('/dashboard')
@auth.login_required
async def dashboard():
    """Dashboard principale con formazioni organizzate per status (Flask Async)."""
    try:
        logger.info("Caricamento dashboard con Flask Async...")
        
        # Inizializzazione NotionService
        notion_service = NotionService()
        logger.info("NotionService inizializzato correttamente")
        
        # PERFORMANCE BOOST: Chiamate parallele con asyncio.gather()
        formazioni_results = await asyncio.gather(
            notion_service.get_formazioni_by_status('Programmata'),
            notion_service.get_formazioni_by_status('Calendarizzata'),
            notion_service.get_formazioni_by_status('Conclusa'),
            return_exceptions=True  # Continua anche se una chiamata fallisce
        )
        
        # Gestione risultati con error handling
        formazioni_programmata = formazioni_results[0] if not isinstance(formazioni_results[0], Exception) else []
        formazioni_calendarizzata = formazioni_results[1] if not isinstance(formazioni_results[1], Exception) else []
        formazioni_conclusa = formazioni_results[2] if not isinstance(formazioni_results[2], Exception) else []
        
        # Statistiche con null safety
        stats = {
            'programmata': len(formazioni_programmata or []),
            'calendarizzata': len(formazioni_calendarizzata or []),
            'conclusa': len(formazioni_conclusa or []),
        }
        stats['totale'] = stats['programmata'] + stats['calendarizzata'] + stats['conclusa']
        
        logger.info(f"Dashboard caricata con successo (Atomic Design). Totale formazioni: {stats['totale']}")
        
        # Usa il nuovo template atomic design
        return render_template('pages/dashboard.html',
                             formazioni_programmata=formazioni_programmata or [],
                             formazioni_calendarizzata=formazioni_calendarizzata or [],
                             formazioni_conclusa=formazioni_conclusa or [],
                             stats=stats,
                             title='Dashboard - Formazing')
                             
    except NotionServiceError as e:
        # Errore specifico NotionService
        logger.error(f"NotionService error: {e}")
        flash(f"❌ Errore servizio Notion: {e}", 'error')
        return redirect(url_for('main.home'))
        
    except Exception as e:
        # Errore generico
        logger.error(f"Errore imprevisto nella dashboard: {e}")
        flash(f"❌ Errore imprevisto: {e}", 'error')
        return redirect(url_for('main.home'))

@main.route('/formazioni/<status>')
@auth.login_required  
async def formazioni_by_status(status):
    """
    Visualizza formazioni filtrate per status (Flask Async).
    NOTA: Questa funzionalità è ora integrata nella dashboard con tab.
    Redirect alla dashboard per ora.
    
    Args:
        status: Programmata, Calendarizzata, o Conclusa
    """
    # Redirect alla dashboard che ha già i tab per status
    return redirect(url_for('main.dashboard'))


@main.route('/api/config/status')
@auth.login_required
async def api_config_status():
    """API endpoint per verificare status configurazione (Flask Async)."""
    try:
        validation = Config.validate_config()
        notion_service = NotionService()
        service_stats = notion_service.get_service_stats()
        
        # 🚀 Test connessione Notion con async
        connection_test = await notion_service.test_connection()
        
        return jsonify({
            'config_validation': validation,
            'notion_service': service_stats,
            'connection_test': connection_test,
            'status': 'ok' if validation['overall_ok'] else 'warning'
        })
        
    except Exception as e:
        logger.error(f"Errore API config status: {e}")
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500


@main.route('/api/formazioni')
@auth.login_required
async def api_formazioni():
    """API endpoint per recuperare formazioni (JSON) con Flask Async."""
    try:
        status = request.args.get('status')
        notion_service = NotionService()
        
        if status:
            # Recupera formazioni per status specifico
            formazioni_data = await notion_service.get_formazioni_by_status(status)
        else:
            # 🚀 Recupera tutte le formazioni in parallelo per performance ottimale
            all_results = await asyncio.gather(
                notion_service.get_formazioni_by_status('Programmata'),
                notion_service.get_formazioni_by_status('Calendarizzata'),
                notion_service.get_formazioni_by_status('Conclusa'),
                return_exceptions=True
            )
            
            # Organizza i risultati per status
            formazioni_data = {
                'programmata': all_results[0] if not isinstance(all_results[0], Exception) else [],
                'calendarizzata': all_results[1] if not isinstance(all_results[1], Exception) else [],
                'conclusa': all_results[2] if not isinstance(all_results[2], Exception) else []
            }
            
        return jsonify({
            'formazioni': formazioni_data,
            'status': 'success'
        })
        
    except NotionServiceError as e:
        logger.error(f"Errore API formazioni: {e}")
        return jsonify({
            'error': f'Errore NotionService: {e}',
            'status': 'error'
        }), 500