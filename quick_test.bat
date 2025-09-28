@echo off
chcp 65001 > nul
echo.
echo 🧪 FORMAZING QUICK TEST RUNNER
echo ===============================

if "%1"=="" (
    echo.
    echo 💡 Uso: quick_test.bat [COMANDO]
    echo.
    echo 📋 COMANDI DISPONIBILI:
    echo    format     - Solo test formattazione ^(sicuro, no invio^)
    echo    safe       - Test sicuri ^(formattazione + diagnostica^)
    echo    interactive - Test completo interattivo ^(chiede conferma per invio^)
    echo    real       - Test con invio reale ^(ATTENZIONE: invia messaggi veri^)
    echo    training   - Solo test invio notifica formazione ^(REALE^)
    echo    feedback   - Solo test invio feedback ^(REALE^)
    echo    bot        - Solo test comandi bot ^(REALE^)
    echo    check      - Verifica setup ambiente
    echo.
    echo 🎯 ESEMPI:
    echo    quick_test.bat format       ^(più sicuro - solo preview^)
    echo    quick_test.bat interactive  ^(raccomandato - test completi^)
    echo    quick_test.bat training     ^(test specifico invio formazione^)
    echo    quick_test.bat real         ^(tutti i test reali^)
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

if "%1"=="format" (
    echo 🎨 Esecuzione test SOLO FORMATTAZIONE ^(sicuro^)...
    echo 💡 Test preview messaggi senza invio reale
    echo ⏳ Avvio pytest...
    python -m pytest tests/integration/test_real_telegram.py::TestRealTelegramIntegration::test_formatter_preview_messages -s -v --tb=short
    goto :end
)

if "%1"=="safe" (
    echo 🛡️ Esecuzione test SICURI ^(no invio reale^)...
    echo 💡 Solo test formattazione e diagnostica
    echo ⏳ Avvio pytest...
    python -m pytest tests/integration/test_real_telegram.py::TestRealTelegramIntegration::test_formatter_preview_messages -s -v --tb=short
    goto :end
)

if "%1"=="interactive" (
    echo 🤖 Esecuzione test INTERATTIVO ^(raccomandato^)...
    echo 💡 Test completi con conferme manuali e verifiche precise
    echo ⏳ Avvio pytest...
    python -m pytest tests/integration/test_real_telegram.py::TestRealTelegramIntegration -s -v --tb=short
    goto :end
)

if "%1"=="training" (
    echo 📤 Esecuzione test INVIO FORMAZIONE ^(REALE^)...
    echo ⚠️ Questo test invierà una notifica formazione reale!
    echo ⏳ Avvio pytest...
    python -m pytest tests/integration/test_real_telegram.py::TestRealTelegramIntegration::test_send_training_notification_real -s -v --tb=short
    goto :end
)

if "%1"=="feedback" (
    echo 📋 Esecuzione test INVIO FEEDBACK ^(REALE^)...
    echo ⚠️ Questo test invierà una richiesta feedback reale!
    echo ⏳ Avvio pytest...
    python -m pytest tests/integration/test_real_telegram.py::TestRealTelegramIntegration::test_send_feedback_notification_real -s -v --tb=short
    goto :end
)

if "%1"=="bot" (
    echo 🤖 Esecuzione test COMANDI BOT ^(REALE^)...
    echo ⚠️ Questo test avvierà il bot reale per 60 secondi!
    echo ⏳ Avvio pytest...
    python -m pytest tests/integration/test_real_telegram.py::TestRealTelegramIntegration::test_bot_commands_interactive -s -v --tb=short
    goto :end
)

if "%1"=="real" (
    echo.
    echo ⚠️  ATTENZIONE: INVIO MESSAGGI REALI ⚠️
    echo 📱 Questo test invierà messaggi sui gruppi Telegram configurati!
    echo 🔍 I messaggi saranno marcati [TEST] ma sono comunque REALI
    echo.
    set /p confirm="❓ Sei sicuro di voler continuare? (S/N): "
    if /i not "%confirm%"=="S" (
        echo ⏭️ Test annullato
        goto :end
    )
    echo.
    echo 🚀 Esecuzione test con INVIO REALE...
    echo 💡 Test precisi con verifiche dettagliate
    echo ⏳ Avvio pytest...
    python -m pytest tests/integration/test_real_telegram.py::TestRealTelegramIntegration -m real_telegram -s -v --tb=short
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