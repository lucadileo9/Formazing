# run_bot.py
import logging
from app.services.training_service import TrainingService
from dotenv import load_dotenv

# Imposta un logging di base per vedere i messaggi del bot e gli eventuali errori
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Carica le variabili d'ambiente dal file .env (necessario per il token)
load_dotenv()

if __name__ == "__main__":
    logger = logging.getLogger(__name__)
    logger.info("Avvio del processo dedicato al Bot Telegram...")
    logger.info("Questo processo gestirà i comandi interattivi come /oggi, /domani, etc.")

    # Ottieni l'istanza del TrainingService.
    # Questo crea e configura in modo sicuro tutti i servizi necessari,
    # incluso il TelegramService, senza però avviare thread.
    training_service = TrainingService.get_instance()

    # Usa il metodo `run_bot_sync` già esistente in TelegramService.
    # Questo metodo è progettato appositamente per scenari come questo:
    # gestisce l'avvio, l'attesa di comandi e lo spegnimento pulito del bot.
    try:
        training_service.telegram_service.run_bot_sync()
    except Exception as e:
        logger.critical(f"Errore critico non gestito nel processo del bot: {e}", exc_info=True)
    
    logger.info("Processo del bot terminato.")
