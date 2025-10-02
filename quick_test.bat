@echo off
chcp 65001 > nul
echo.
echo 🧪 FORMAZING QUICK TEST RUNNER
echo ===============================

if "%1"=="" (
    echo.
    echo 💡 Uso: quick_test.bat [COMANDO]
    echo.
    echo 🎯 COMANDI PIÙ USATI:
    echo   unit     - Test unitari (1.2s)
    echo   notion   - Test NotionService (0.9s)
    echo   config   - Verifica connessioni
    echo   workflow - Test workflow completo
    echo   send     - Invio controllato con conferma
    echo.
    echo 📚 Per lista completa comandi: docs/testing/README.md
    echo.
    goto :end
)

echo 🔧 Setup ambiente...
if not exist ".env" (
    echo ❌ File .env non trovato!
    echo 💡 Crea il file .env con TELEGRAM_BOT_TOKEN=your_token_here
    goto :error
)

if not exist "tests\config\test_telegram_groups.json" (
    echo ❌ File tests\config\test_telegram_groups.json non trovato!
    echo 💡 Configura i gruppi Telegram di test
    goto :error
)

if not exist "tests\config\test_message_templates.yaml" (
    echo ❌ File tests\config\test_message_templates.yaml non trovato!
    echo 💡 Configura i template messaggi di test
    goto :error
)

if "%1"=="check" (
    echo ✅ Tutti i file di configurazione sono presenti
    echo 🔍 Verifica ambiente Python...
    python -c "import pytest; print('✅ pytest disponibile')" 2>nul || (
        echo ❌ pytest non installato
        echo 💡 Installa con: pip install pytest
        goto :error
    )
    echo 🎉 Ambiente configurato correttamente!
    goto :end
)

if "%1"=="unit" (
    echo ⚡ Test unitari ^(1.2s^)...
    python -m pytest tests/unit/ -v
    goto :end
)

if "%1"=="notion" (
    echo 🗃️ Test NotionService ^(0.9s^)...
    python -m pytest tests/unit/notion/ -v
    goto :end
)

if "%1"=="format" (
    echo 🎨 Test formattazione messaggi...
    python -m pytest tests/integration/test_real_telegram.py::TestRealTelegramIntegration::test_formatter_preview_messages -s -v --tb=short
    goto :end
)

if "%1"=="safe" (
    echo 🛡️ Test sicuri ^(no invio^)...
    python -m pytest tests/integration/test_real_telegram.py::TestRealTelegramIntegration::test_formatter_preview_messages -s -v --tb=short
    goto :end
)

if "%1"=="interactive" (
    echo 🤖 Test interattivi con conferme...
    python -m pytest tests/integration/test_real_telegram.py::TestRealTelegramIntegration -s -v --tb=short
    goto :end
)

if "%1"=="training" (
    echo 📤 Test invio formazione ^(REALE^)...
    python -m pytest tests/integration/test_real_telegram.py::TestRealTelegramIntegration::test_send_training_notification_real -s -v --tb=short
    goto :end
)

if "%1"=="feedback" (
    echo 📋 Test feedback ^(REALE^)...
    python -m pytest tests/integration/test_real_telegram.py::TestRealTelegramIntegration::test_send_feedback_notification_real -s -v --tb=short
    goto :end
)

if "%1"=="bot" (
    echo 🤖 Test bot ^(REALE 60s^)...
    python -m pytest tests/integration/test_real_telegram.py::TestRealTelegramIntegration::test_bot_commands_interactive -s -v --tb=short
    goto :end
)

if "%1"=="real" (
    echo 🚨 Test tutti reali...
    set /p confirm="❓ Continui? (S/N): "
    if /i not "%confirm%"=="S" (
        echo ⏭️ Annullato
        goto :end
    )
    python -m pytest tests/integration/test_real_telegram.py::TestRealTelegramIntegration -m real_telegram -s -v --tb=short
    goto :end
)

if "%1"=="config" (
    echo 🔍 Verifica connessioni...
    python tests\e2e\test_real_config.py
    goto :end
)

if "%1"=="preview" (
    echo 🎨 Test formattazione con dati reali...
    python tests\e2e\test_real_formatting.py
    goto :end
)

if "%1"=="send" (
    echo 📤 Test invio controllato...
    echo ⚠️ ATTENZIONE: Può inviare messaggi REALI dopo conferma!
    python tests\e2e\test_real_send.py
    goto :end
)

if "%1"=="workflow" (
    echo 🔄 Test workflow completo ^(safe^)...
    python tests\e2e\test_workflow.py --limit 3
    goto :end
)

if "%1"=="workflow-real" (
    echo 🔄 Workflow reale...
    python tests\e2e\test_workflow.py --real --limit 2
    goto :end
)

echo ❌ Comando non riconosciuto: %1
echo 💡 Usa: quick_test.bat (senza parametri) per vedere l'help
goto :error

:error
echo.
echo ❌ Errore nell'esecuzione
exit /b 1

:end
echo.
echo ✅ Operazione completata