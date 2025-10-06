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
from app.services.training_service import TrainingService, TrainingServiceError
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


# === PAGINE PREVIEW CON FORM CONFERMA ===

@main.route('/preview/notification/<training_id>')
@auth.login_required
async def preview_notification_page(training_id):
    """Pagina preview calendarizzazione con form conferma."""
    try:
        logger.info(f"📄 Apertura preview calendarizzazione per {training_id}")
        
        # Genera preview usando TrainingService
        training_service = TrainingService()
        preview_data = await training_service.generate_preview(training_id)
        
        # Renderizza template preview
        return render_template('pages/preview.html',
                             preview=preview_data,
                             action_type='notification',
                             action_title='Calendarizzazione Formazione',
                             action_icon='📅',
                             training_id=training_id,
                             title=f"Preview - {preview_data['training']['Nome']}")
        
    except TrainingServiceError as e:
        logger.error(f"Errore preview notification: {e}")
        flash(f'❌ Errore: {e}', 'error')
        return redirect(url_for('main.dashboard'))
    except Exception as e:
        logger.error(f"Errore imprevisto preview notification: {e}")
        flash(f'❌ Errore imprevisto: {e}', 'error')
        return redirect(url_for('main.dashboard'))


@main.route('/preview/feedback/<training_id>')
@auth.login_required
async def preview_feedback_page(training_id):
    """Pagina preview richiesta feedback con form conferma."""
    try:
        logger.info(f"📄 Apertura preview feedback per {training_id}")
        
        # Genera preview usando TrainingService
        training_service = TrainingService()
        preview_data = await training_service.generate_feedback_preview(training_id)
        
        # Renderizza template preview
        return render_template('pages/preview.html',
                             preview=preview_data,
                             action_type='feedback',
                             action_title='Richiesta Feedback',
                             action_icon='📝',
                             training_id=training_id,
                             title=f"Preview Feedback - {preview_data['training']['Nome']}")
        
    except TrainingServiceError as e:
        logger.error(f"Errore preview feedback: {e}")
        flash(f'❌ Errore: {e}', 'error')
        return redirect(url_for('main.dashboard'))
    except Exception as e:
        logger.error(f"Errore imprevisto preview feedback: {e}")
        flash(f'❌ Errore imprevisto: {e}', 'error')
        return redirect(url_for('main.dashboard'))


@main.route('/confirm/notification/<training_id>', methods=['POST'])
@auth.login_required
async def confirm_notification(training_id):
    """Conferma ed esegue calendarizzazione (chiamata da form preview)."""
    try:
        logger.info(f"✅ Conferma calendarizzazione per {training_id}")
        
        # Esegui workflow completo
        training_service = TrainingService()
        result = await training_service.send_training_notification(training_id)
        
        logger.info(f"Calendarizzazione completata - Codice: {result['codice_generato']}")
        flash('✅ Comunicazione inviata con successo! La formazione è stata calendarizzata.', 'success')
        
        # Redirect a dashboard
        return redirect(url_for('main.dashboard'))
        
    except TrainingServiceError as e:
        logger.error(f"Errore conferma notification: {e}")
        flash(f'❌ Errore: {e}', 'error')
        return redirect(url_for('main.dashboard'))
    except Exception as e:
        logger.error(f"Errore imprevisto conferma notification: {e}")
        flash(f'❌ Errore imprevisto: {e}', 'error')
        return redirect(url_for('main.dashboard'))


@main.route('/confirm/feedback/<training_id>', methods=['POST'])
@auth.login_required
async def confirm_feedback(training_id):
    """Conferma ed esegue invio feedback (chiamata da form preview)."""
    try:
        logger.info(f"✅ Conferma feedback per {training_id}")
        
        # Esegui workflow feedback
        training_service = TrainingService()
        result = await training_service.send_feedback_request(training_id)
        
        logger.info("Feedback inviato con successo")
        flash('✅ Richiesta feedback inviata con successo! La formazione è stata conclusa.', 'success')
        
        # Redirect a dashboard
        return redirect(url_for('main.dashboard'))
        
    except TrainingServiceError as e:
        logger.error(f"Errore conferma feedback: {e}")
        flash(f'❌ Errore: {e}', 'error')
        return redirect(url_for('main.dashboard'))
    except Exception as e:
        logger.error(f"Errore imprevisto conferma feedback: {e}")
        flash(f'❌ Errore imprevisto: {e}', 'error')
        return redirect(url_for('main.dashboard'))
