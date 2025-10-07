@echo off
chcp 65001 > nul
echo.
echo 🧪 FORMAZING QUICK TEST RUNNER
echo ===============================



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

if "%1"=="microsoft" (
    echo 🔷 Test Microsoft Service ^(isolato^)...
    python tests\e2e\test_real_microsoft.py
    goto :end
)

if "%1"=="integration" (
    echo 🔗 Test integrazione Notion → Microsoft...
    python tests\integration\test_notion_microsoft_integration.py
    goto :end
)

if "%1"=="teams" (
    echo 📅 Test completo Microsoft Teams...
    echo.
    echo 📋 Piano test Microsoft:
    echo   1️⃣ Test service isolato ^(crea evento + email^)
    echo   2️⃣ Test integrazione Notion → Microsoft
    echo.
    set /p confirm1="❓ Esegui test isolato Microsoft? (S/N): "
    if /i "%confirm1%"=="S" (
        echo 🔷 Test Microsoft Service...
        python tests\e2e\test_real_microsoft.py
        if %errorlevel% neq 0 (
            echo ❌ Test Microsoft fallito
            goto :error
        )
        echo ✅ Test Microsoft completato!
        echo.
    )
    
    set /p confirm2="❓ Esegui test integrazione Notion → Microsoft? (S/N): "
    if /i "%confirm2%"=="S" (
        echo 🔗 Test integrazione...
        python tests\integration\test_notion_microsoft_integration.py
        if %errorlevel% neq 0 (
            echo ❌ Test integrazione fallito
            goto :error
        )
        echo ✅ Test integrazione completato!
    )
    echo.
    echo 🎉 Suite test Microsoft completata!
    goto :end
)

if "%1"=="all" (
    echo 🚀 SUITE COMPLETA PRE-COMMIT
    echo.
    echo 📋 Piano di test:
    echo   1️⃣ Test unitari ^(106 test, 1.2s^)
    echo   2️⃣ Verifica connessioni ^(Notion + Telegram^) 
    echo   3️⃣ Test formattazione ^(template con dati reali^)
    echo   4️⃣ Workflow simulazione ^(processo completo safe^)
    echo.
    
    echo 🟦 STEP 1/4 - Test Unitari
    echo ===========================
    echo 🎯 Esegue: 106 test unitari ^(NotionService + TelegramFormatter^)
    echo.

    echo ⏳ Attendi 5 secondi prima di iniziare...
    timeout /t 5 > nul

    echo ⚡ Esecuzione test unitari...
    python -m pytest tests/unit/ -v --tb=short
    if %errorlevel% neq 0 (
        echo ❌ Test unitari falliti - Interrompo la suite
        goto :error
    )
    echo ✅ Test unitari completati con successo!
    echo.
    
    :step2
    echo 🟨 STEP 2/4 - Verifica Connessioni  
    echo ====================================
    echo 🎯 Esegue: Test connessioni Notion + Telegram
    echo 🛡️ Sicurezza: Solo verifica connessioni, zero invii
    echo 📊 Risultato: Mostra stats formazioni e gruppi configurati
    echo.

    echo ⏳ Attendi 5 secondi prima di iniziare...
    timeout /t 5 > nul

    echo 🔍 Verifica connessioni...
    python tests\e2e\test_real_config.py
    if %errorlevel% neq 0 (
        echo ❌ Problemi connessioni - Verifica .env e config/
        echo 💡 Vuoi continuare comunque? ^(Spesso non bloccante^)
        set /p continueAnyway="❓ Continua con i test successivi? (S/N): "
        if /i not "%continueAnyway%"=="S" (
            echo ⏭️ Suite interrotta dall'utente
            goto :end
        )
    )
    echo ✅ Connessioni verificate!
    echo.
    
    :step3
    echo 🟩 STEP 3/4 - Test Formattazione
    echo =================================
    echo 🎯 Esegue: Formattazione template con 27+ formazioni reali
    echo 🛡️ Sicurezza: Solo generazione preview, zero invii
    echo 📝 Risultato: Valida template YAML e formattazione Markdown
    echo.
    
    echo ⏳ Attendi 5 secondi prima di iniziare...
    timeout /t 5 > nul

    echo 🎨 Test formattazione messaggi...
    python tests\e2e\test_real_formatting.py
    if %errorlevel% neq 0 (
        echo ❌ Problemi formattazione template - Controlla config/
        goto :error
    )
    echo ✅ Formattazione validata!
    echo.
    
    :step4
    echo 🟪 STEP 4/4 - Workflow Simulazione
    echo ==================================
    echo 🎯 Esegue: Workflow completo con 3 formazioni reali
    echo 🛡️ Sicurezza: Simulazione completa, zero modifiche database
    echo 🔄 Processo: Preview → Generazione codici → Formattazione → Report
    echo.
    
    echo ⏳ Attendi 5 secondi prima di iniziare...
    timeout /t 5 > nul

    echo 🔄 Workflow simulazione...
    python tests\e2e\test_workflow.py --limit 3
    if %errorlevel% neq 0 (
        echo ❌ Problemi workflow - Verifica logica integrazione
        goto :error
    )
    echo ✅ Workflow simulato con successo!
    echo.
    
    :summary
    echo 🎉 SUITE COMPLETA TERMINATA
    echo ✅ Tutti i test sono stati completati con successo!
    echo.
    goto :end
)

if "%1"=="" (
    echo.
    echo 💡 Uso: quick_test.bat [COMANDO]
    echo.
    echo 🎯 COMANDI PIÙ USATI:
    echo   unit     - Test unitari (1.2s)
    echo   notion   - Test NotionService (0.9s)
    echo   config   - Verifica connessioni
    echo   workflow - Test workflow completo
    echo   all      - Suite completa pre-commit (interattiva)
    echo   send     - Invio controllato con conferma
    echo.
    echo 🔷 TEST MICROSOFT TEAMS:
    echo   microsoft   - Test Microsoft Service isolato
    echo   integration - Test integrazione Notion → Microsoft
    echo   teams       - Suite completa test Microsoft
    echo.
    echo 📚 Per lista completa comandi: docs/testing/README.md
    echo.
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