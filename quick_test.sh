#!/bin/bash

echo ""
echo "🧪 FORMAZING QUICK TEST RUNNER"
echo "==============================="

show_help() {
    echo ""
    echo "💡 Uso: ./quick_test.sh [COMANDO]"
    echo ""
    echo "📋 COMANDI DISPONIBILI:"
    echo "   format     - Solo test formattazione (sicuro, no invio)"
    echo "   safe       - Test sicuri (formattazione + diagnostica)"
    echo "   interactive - Test completo interattivo (chiede conferma per invio)"
    echo "   real       - Test con invio reale (ATTENZIONE: invia messaggi veri)"
    echo "   check      - Verifica setup ambiente"
    echo ""
    echo "🎯 ESEMPI:"
    echo "   ./quick_test.sh format       (più sicuro)"
    echo "   ./quick_test.sh interactive  (raccomandato)"
    echo "   ./quick_test.sh real         (solo se sicuro)"
    echo ""
}

check_prerequisites() {
    echo "🔧 Setup ambiente..."
    
    if [ ! -f ".env" ]; then
        echo "❌ File .env non trovato!"
        echo "💡 Crea il file .env con TELEGRAM_BOT_TOKEN=your_token_here"
        exit 1
    fi

    if [ ! -f "tests/config/test_telegram_groups.json" ]; then
        echo "❌ File tests/config/test_telegram_groups.json non trovato!"
        echo "💡 Configura i gruppi Telegram di test"
        exit 1
    fi

    if [ ! -f "tests/config/test_message_templates.yaml" ]; then
        echo "❌ File tests/config/test_message_templates.yaml non trovato!"
        echo "💡 Configura i template messaggi di test"
        exit 1
    fi
}

if [ -z "$1" ]; then
    show_help
    exit 0
fi

case "$1" in
    "check")
        check_prerequisites
        echo "✅ Tutti i file di configurazione sono presenti"
        echo "🔍 Verifica ambiente Python..."
        python3 -c "import pytest; print('✅ pytest disponibile')" 2>/dev/null || {
            echo "❌ pytest non installato" 
            echo "💡 Installa con: pip install pytest"
            exit 1
        }
        echo "🎉 Ambiente configurato correttamente!"
        ;;
        
    "format")
        check_prerequisites
        echo "🎨 Esecuzione test SOLO FORMATTAZIONE (sicuro)..."
        echo "⏳ Avvio pytest..."
        python3 -m pytest tests/quick_real_test.py::test_quick_interactive -s -k "not send" --tb=short
        ;;
        
    "safe")
        check_prerequisites
        echo "🛡️ Esecuzione test SICURI (no invio reale)..."
        echo "⏳ Avvio pytest..."
        python3 -m pytest tests/quick_real_test.py::test_quick_interactive -s --tb=short
        echo ""
        echo "💡 TIP: Durante il test, rispondi 'N' a tutte le richieste di invio reale"
        ;;
        
    "interactive")
        check_prerequisites
        echo "🤖 Esecuzione test INTERATTIVO (raccomandato)..."
        echo "💡 Il test ti chiederà cosa fare per ogni step"
        echo "⏳ Avvio pytest..."
        python3 -m pytest tests/quick_real_test.py::test_quick_interactive -s -v --tb=short
        ;;
        
    "real")
        check_prerequisites
        echo ""
        echo "⚠️  ATTENZIONE: INVIO MESSAGGI REALI ⚠️"
        echo "📱 Questo test invierà messaggi sui gruppi Telegram configurati!"
        echo "🔍 I messaggi saranno marcati [TEST] ma sono comunque REALI"
        echo ""
        read -p "❓ Sei sicuro di voler continuare? (s/N): " confirm
        if [[ ! "$confirm" =~ ^[Ss]$ ]]; then
            echo "⏭️ Test annullato"
            exit 0
        fi
        echo ""
        echo "🚀 Esecuzione test con INVIO REALE..."
        echo "⏳ Avvio pytest..."
        python3 -m pytest tests/quick_real_test.py::test_quick_interactive -s -v --tb=short
        echo ""
        echo "💡 TIP: Durante il test, rispondi 'Y' alle richieste di invio per testare"
        ;;
        
    *)
        echo "❌ Comando non riconosciuto: $1"
        echo "💡 Usa: ./quick_test.sh (senza parametri) per vedere l'help"
        exit 1
        ;;
esac

echo ""
echo "✅ Operazione completata"