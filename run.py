#!/usr/bin/env python3
"""
🚀 Formazing - App Gestione Formazioni
Entry point principale per l'applicazione Flask

UTILIZZO:
python run.py

ACCESSO:
http://localhost:5000
Username/Password: configurabili in config.py
"""

from app import create_app
from config import Config

# Crea l'applicazione Flask
app = create_app()

if __name__ == '__main__':
    print("=" * 60)
    print("🚀 FORMAZING - APP GESTIONE FORMAZIONI")
    print("=" * 60)
    print(f"📍 URL: http://localhost:{Config.FLASK_PORT}")
    print(f"🔐 Auth: Basic Auth richiesta")
    print(f"🏠 Home: Dashboard formazioni")
    print("=" * 60)
    
    # Avvia il server Flask
    app.run(
        host='0.0.0.0',
        port=Config.FLASK_PORT,
        debug=Config.DEBUG,
        threaded=True
    )