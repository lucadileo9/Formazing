#!/bin/bash

echo ""
echo "🧪 FORMAZING QUICK TEST RUNNER"
echo "==============================="

show_help() {
    echo ""
    echo "💡 Uso: ./quick_test.sh [COMANDO]"
    echo ""
    echo "🎯 COMANDI PIÙ USATI:"
    echo "   unit     - Test unitari (1.2s)"
    echo "   notion   - Test NotionService (0.9s)"
    echo "   config   - Verifica connessioni"
    echo "   workflow - Test workflow completo"
    echo "   send     - Invio controllato con conferma"
    echo ""
    echo "🔷 TEST MICROSOFT TEAMS:"
    echo "   microsoft   - Test Microsoft Service isolato"
    echo "   integration - Test integrazione Notion → Microsoft"
    echo "   teams       - Suite completa test Microsoft"
    echo ""
    echo "📚 Per lista completa comandi: docs/testing/README.md"
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

check_prerequisites

case "$1" in
    "check")
        echo "✅ Tutti i file di configurazione sono presenti"
        echo "🔍 Verifica ambiente Python..."
        python3 -c "import pytest; print('✅ pytest disponibile')" 2>/dev/null || {
            echo "❌ pytest non installato" 
            echo "💡 Installa con: pip install pytest"
            exit 1
        }
        echo "🎉 Ambiente configurato correttamente!"
        ;;
        
    "unit")
        echo "⚡ Test unitari (1.2s)..."
        python3 -m pytest tests/unit/ -v
        ;;
        
    "notion")
        echo "🗃️ Test NotionService (0.9s)..."
        python3 -m pytest tests/unit/notion/ -v
        ;;
        
    "format")
        echo "🎨 Test formattazione messaggi..."
        python3 -m pytest tests/integration/test_real_telegram.py::TestRealTelegramIntegration::test_formatter_preview_messages -s -v --tb=short
        ;;
        
    "safe")
        echo "🛡️ Test sicuri (no invio)..."
        python3 -m pytest tests/integration/test_real_telegram.py::TestRealTelegramIntegration::test_formatter_preview_messages -s -v --tb=short
        ;;
        
    "interactive")
        echo "🤖 Test interattivi con conferme..."
        python3 -m pytest tests/integration/test_real_telegram.py::TestRealTelegramIntegration -s -v --tb=short
        ;;
        
    "training")
        echo "📤 Test invio formazione (REALE)..."
        python3 -m pytest tests/integration/test_real_telegram.py::TestRealTelegramIntegration::test_send_training_notification_real -s -v --tb=short
        ;;
        
    "feedback")
        echo "📋 Test feedback (REALE)..."
        python3 -m pytest tests/integration/test_real_telegram.py::TestRealTelegramIntegration::test_send_feedback_notification_real -s -v --tb=short
        ;;
        
    "bot")
        echo "🤖 Test bot (REALE 60s)..."
        python3 -m pytest tests/integration/test_real_telegram.py::TestRealTelegramIntegration::test_bot_commands_interactive -s -v --tb=short
        ;;
        
    "real")
        echo "🚨 Test tutti reali..."
        read -p "❓ Continui? (s/N): " confirm
        if [[ ! "$confirm" =~ ^[Ss]$ ]]; then
            echo "⏭️ Annullato"
            exit 0
        fi
        python3 -m pytest tests/integration/test_real_telegram.py::TestRealTelegramIntegration -m real_telegram -s -v --tb=short
        ;;
        
    "config")
        echo "� Verifica connessioni..."
        python3 tests/e2e/test_real_config.py
        ;;
        
    "preview")
        echo "🎨 Test formattazione con dati reali..."
        python3 tests/e2e/test_real_formatting.py
        ;;
        
    "send")
        echo "📤 Test invio controllato..."
        echo "⚠️ ATTENZIONE: Può inviare messaggi REALI dopo conferma!"
        python3 tests/e2e/test_real_send.py
        ;;
        
    "workflow")
        echo "🔄 Test workflow completo (safe)..."
        python3 tests/e2e/test_workflow.py --limit 3
        ;;
        
    "workflow-real")
        echo "🔄 Workflow reale..."
        python3 tests/e2e/test_workflow.py --real --limit 2
        ;;
        
    "microsoft")
        echo "🔷 Test Microsoft Service (isolato)..."
        python3 tests/e2e/test_real_microsoft.py
        ;;
        
    "integration")
        echo "🔗 Test integrazione Notion → Microsoft..."
        python3 tests/integration/test_notion_microsoft_integration.py
        ;;
        
    "teams")
        echo "📅 Test completo Microsoft Teams..."
        echo ""
        echo "📋 Piano test Microsoft:"
        echo "   1️⃣ Test service isolato (crea evento + email)"
        echo "   2️⃣ Test integrazione Notion → Microsoft"
        echo ""
        
        read -p "❓ Esegui test isolato Microsoft? (s/N): " confirm1
        if [[ "$confirm1" =~ ^[Ss]$ ]]; then
            echo "🔷 Test Microsoft Service..."
            python3 tests/e2e/test_real_microsoft.py
            if [ $? -ne 0 ]; then
                echo "❌ Test Microsoft fallito"
                exit 1
            fi
            echo "✅ Test Microsoft completato!"
            echo ""
        fi
        
        read -p "❓ Esegui test integrazione Notion → Microsoft? (s/N): " confirm2
        if [[ "$confirm2" =~ ^[Ss]$ ]]; then
            echo "🔗 Test integrazione..."
            python3 tests/integration/test_notion_microsoft_integration.py
            if [ $? -ne 0 ]; then
                echo "❌ Test integrazione fallito"
                exit 1
            fi
            echo "✅ Test integrazione completato!"
        fi
        
        echo ""
        echo "🎉 Suite test Microsoft completata!"
        ;;
        
    *)
        echo "❌ Comando non riconosciuto: $1"
        echo "💡 Usa: ./quick_test.sh (senza parametri) per vedere l'help"
        exit 1
        ;;
esac

echo ""
echo "✅ Operazione completata"