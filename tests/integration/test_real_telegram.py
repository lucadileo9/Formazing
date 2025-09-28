"""
Test Integration Reali - Solo Notion è mock, tutto il resto è REALE!

Questi test usano:
✅ TelegramService REALE con bot vero
✅ TelegramFormatter REALE con template veri  
✅ TelegramCommands REALE con logica vera
✅ Invio messaggi REALI su Telegram
❌ Solo NotionService è mock

REQUISITI per eseguire questi test:
1. TELEGRAM_BOT_TOKEN valido nel file .env
2. Gruppi Telegram di test configurati in tests/config/test_telegram_groups.json
3. Bot aggiunto a tutti i gruppi di test
4. Connessione internet attiva

SAFETY:
- I test inviano messaggi REALI ma SOLO sui gruppi di test
- Messaggi chiaramente marcati [TEST]
- Nessun impatto su dati Notion (sempre mock)
- Possibilità di eseguire test senza invio reale
"""

import asyncio
import pytest
from datetime import datetime, timedelta


class TestRealTelegramIntegration:
    """
    Test Integration con componenti Telegram REALI -
    
    USA TUTTE LE FIXTURE da conftest.py:
    ✅ configured_telegram_service: Service completo pronto all'uso
    ✅ sample_training_data: Dati standard centralizzati
    ✅ sample_feedback_data: Dati feedback centralizzati
    ✅ load_test_env: Configurazioni ambiente
    ✅ mock_notion_service: Mock già configurato
    
    """
    
    @pytest.mark.asyncio
    @pytest.mark.real_telegram
    async def test_send_training_notification_real(
        self, 
        configured_telegram_service, 
        sample_training_data          
    ):
        """
        Test REALE invio notifica training - Focus su risultati visibili.
        
        USA FIXTURE:
        - configured_telegram_service: TelegramService + MockNotionService già configurati
        - sample_training_data: Dati standard da conftest.py
        
        OBIETTIVO: Vedere che i messaggi arrivano con i dati giusti.
        """
        print(f"\n📤 Invio notifica training...")
        print(f"📊 Formazione: {sample_training_data['Nome']}")  
        print(f"🎯 Area: {sample_training_data['Area']}")
        print(f"📅 Data: {sample_training_data['Data/Ora']}")
        
        # ✅ ANTEPRIMA: Mostra cosa verrà inviato
        formatter = configured_telegram_service.formatter
        main_msg = formatter.format_training_message(sample_training_data, 'main_group')
        area_msg = formatter.format_training_message(sample_training_data, 'area_group')
        
        print(f"\n📄 ANTEPRIMA MESSAGGIO MAIN GROUP:")
        print(f"{'='*60}")
        print(main_msg)
        print(f"{'='*60}")
        
        print(f"\n📄 ANTEPRIMA MESSAGGIO AREA GROUP ({sample_training_data['Area']}):")
        print(f"{'='*60}")
        print(area_msg)
        print(f"{'='*60}")
        
        # ✅ INVIO REALE
        results = await configured_telegram_service.send_training_notification(sample_training_data)
        
        # ✅ VERIFICA SEMPLICE E UTILE
        assert isinstance(results, dict), "Risultati devono essere dizionario"
        assert 'main_group' in results, "Deve inviare a main_group"
        assert sample_training_data['Area'] in results, "Deve inviare a gruppo area"
        
        successful_sends = sum(1 for success in results.values() if success)
        failed_sends = [group for group, success in results.items() if not success]
        
        print(f"\n✅ RISULTATI INVIO:")
        print(f"📤 Inviati: {successful_sends}/{len(results)} gruppi")
        print(f"📱 Gruppi raggiunti: {list(results.keys())}")
        
        if failed_sends:
            print(f"❌ Invii falliti: {failed_sends}")
        
        print(f"\n🔍 Ora controlla i gruppi Telegram:")
        print(f"   1. Gruppo main_group → messaggio generale")
        print(f"   2. Gruppo {sample_training_data['Area']} → messaggio specifico area")
        print(f"   3. Verifica che i dati siano corretti (nome, data, link)")
        
        # Pausa per verifica manuale
        input("👀 Premi INVIO dopo aver controllato i messaggi su Telegram...")
        
        assert successful_sends >= 2, f"Almeno 2 gruppi devono ricevere il messaggio"
    
    @pytest.mark.asyncio
    @pytest.mark.real_telegram
    async def test_send_feedback_notification_real(
        self, 
        configured_telegram_service,   
        sample_feedback_data          
    ):
        """
        Test REALE invio richiesta feedback - Focus su risultati visibili.
        
        USA FIXTURE:
        - configured_telegram_service: Service già configurato
        - sample_feedback_data: Dati feedback standard
        
        OBIETTIVO: Vedere che il messaggio feedback arrivi correttamente.
        
        COMPORTAMENTO ATTESO:
        - Feedback va SOLO ai gruppi area (anti-spam)
        - NON viene inviato al main_group
        - Include link cliccabile per il form feedback
        """
        feedback_link = 'https://forms.office.com/r/test-feedback-from-fixture'
        
        print(f"\n📝 Invio richiesta feedback...")
        print(f"📚 Formazione: {sample_feedback_data['Nome']}")  
        print(f"🎯 Area: {sample_feedback_data['Area']}")
        print(f"🔗 Link feedback: {feedback_link}")
        
        # ✅ ANTEPRIMA: Mostra cosa verrà inviato
        formatter = configured_telegram_service.formatter
        feedback_msg = formatter.format_feedback_message(
            sample_feedback_data,
            feedback_link,
            'message'
        )
        
        print(f"\n📄 ANTEPRIMA MESSAGGIO FEEDBACK:")
        print(f"{'='*60}")
        print(feedback_msg)
        print(f"{'='*60}")
        
        # ✅ INVIO REALE
        results = await configured_telegram_service.send_feedback_notification(
            sample_feedback_data,  
            feedback_link
        )
        
        # ✅ VERIFICA CORRETTA - Feedback va SOLO ai gruppi area, NON main_group
        assert isinstance(results, dict)
        assert sample_feedback_data['Area'] in results, "Deve inviare a gruppo area corretto"
        assert 'main_group' not in results, "Feedback NON deve andare al main_group (anti-spam)"
        
        successful_sends = sum(1 for success in results.values() if success)
        failed_sends = [group for group, success in results.items() if not success]
        
        print(f"\n✅ RISULTATI INVIO FEEDBACK:")
        print(f"📤 Inviati: {successful_sends}/{len(results)} gruppi")
        print(f"📱 Gruppi raggiunti: {list(results.keys())}")
        
        if failed_sends:
            print(f"❌ Invii falliti: {failed_sends}")
        
        print(f"\n🔍 Ora controlla i gruppi Telegram:")
        print(f"   1. Il messaggio è arrivato SOLO al gruppo {sample_feedback_data['Area']} (non main_group)")
        print(f"   2. Verifica che il link feedback sia cliccabile")
        print(f"   3. Controlla che i dati formazione siano corretti")
        print(f"   4. Messaggio chiaramente marcato come [TEST]")
        print(f"   📋 NOTA: Feedback va solo ai gruppi area (comportamento corretto)")
        
        # Pausa per verifica manuale
        input("👀 Premi INVIO dopo aver controllato il messaggio feedback su Telegram...")
        
        assert successful_sends >= 1, "Almeno un gruppo deve ricevere feedback"
    
    @pytest.mark.asyncio  
    @pytest.mark.real_telegram
    async def test_bot_commands_interactive(
        self, 
        configured_telegram_service,   
        mock_notion_service           
    ):
        """
        Test comandi bot - Focus su risposta e usabilità.
        
        USA FIXTURE:
        - configured_telegram_service: Service configurato
        - mock_notion_service: Per ottenere info sui dati mock
        
        OBIETTIVO: Vedere che il bot risponde con dati sensati.
        """
        print(f"\n🤖 Test comandi bot interattivo...")
        
        # ✅ INFO DATI MOCK (quello che ci aspettiamo)
        mock_info = mock_notion_service.get_current_test_info()
        print(f"📅 MockNotionService configurato:")
        print(f"   • Formazioni oggi: {mock_info['today_formazioni']}")
        print(f"   • Formazioni domani: {mock_info['tomorrow_formazioni']}")
        print(f"   • Formazioni settimana: {mock_info['week_formazioni']}")
        
        print(f"\n💡 Comandi da testare su Telegram:")
        print(f"   /oggi → Deve mostrare {mock_info['today_formazioni']} formazioni")
        print(f"   /domani → Deve mostrare {mock_info['tomorrow_formazioni']} formazione")
        print(f"   /settimana → Deve mostrare circa {mock_info['week_formazioni']} formazioni")
        print(f"   /help → Mostra lista comandi")
        
        try:
            await configured_telegram_service.start_bot()
            print(f"✅ Bot avviato - Apri Telegram e testa i comandi!")
            print(f"⏰ Test per 60 secondi...")
            
            await asyncio.sleep(60)
            
        except KeyboardInterrupt:
            print(f"\n⌨️ Test fermato manualmente")
        finally:
            await configured_telegram_service.stop_bot()
            print(f"✅ Bot fermato")
            
        print(f"\n📋 CHECKLIST RISULTATI (verifica manuale):")
        print(f"   1. /oggi → Ha mostrato {mock_info['today_formazioni']} formazioni? [Y/n]")
        print(f"   2. /domani → Ha mostrato {mock_info['tomorrow_formazioni']} formazione? [Y/n]")
        print(f"   3. /settimana → Ha mostrato circa {mock_info['week_formazioni']} formazioni? [Y/n]")
        print(f"   4. /help → Ha mostrato la lista dei comandi? [Y/n]")
        print(f"   5. Tutti i messaggi erano marcati [TEST]? [Y/n]")
        
        print(f"\n❓ I comandi hanno funzionato correttamente? (Y/n): ", end='')
        user_confirm = input().lower().strip()
        
        # Default a 'y' se vuoto (enter semplice)
        if user_confirm in ['', 'y', 'yes', 's', 'si']:
            print(f"✅ Test comandi completato con successo!")
        else:
            print(f"❌ Dettagli del problema:")
            problem = input(f"Descrivi cosa non ha funzionato: ")
            pytest.fail(f"Comandi bot non hanno funzionato: {problem}")
        
        print(f"💡 TIP: Se alcuni comandi non funzionano, verifica che il bot sia nei gruppi giusti")
    
    @pytest.mark.asyncio
    async def test_formatter_preview_messages(
        self, 
        configured_telegram_service,   
        sample_training_data,         
        alternative_training_data,      
        sample_feedback_data          
    ):
        """
        Test formatter - Anteprima messaggi senza invio (debug veloce).
        
        USA FIXTURE:
        - configured_telegram_service: Service configurato
        - sample_training_data: Dati IT
        - alternative_training_data: Dati HR 
        - sample_feedback_data: Dati feedback
        
        OBIETTIVO: Vedere come appaiono i messaggi formattati.
        """
        print(f"\n🎨 Anteprima formattazione messaggi...")
        
        formatter = configured_telegram_service.formatter
        
        # ✅ TRAINING IT
        main_msg = formatter.format_training_message(sample_training_data, 'main_group')
        print(f"\n📄 TRAINING IT - MAIN GROUP:")
        print(f"{'='*50}")
        print(main_msg)
        print(f"{'='*50}")
        
        # ✅ TRAINING HR  
        area_msg = formatter.format_training_message(alternative_training_data, 'area_group')
        print(f"\n📄 TRAINING HR - AREA GROUP:")
        print(f"{'='*50}")
        print(area_msg)
        print(f"{'='*50}")
        
        # ✅ FEEDBACK
        feedback_msg = formatter.format_feedback_message(
            sample_feedback_data,
            'https://forms.office.com/test-feedback-fixture',
            'message'
        )
        print(f"\n📄 RICHIESTA FEEDBACK:")
        print(f"{'='*50}")
        print(feedback_msg)
        print(f"{'='*50}")
        
        # ✅ VERIFICHE SEMPLICI (i dati sono presenti)
        assert sample_training_data['Nome'] in main_msg, "Nome training IT mancante"
        assert alternative_training_data['Nome'] in area_msg, "Nome training HR mancante"
        assert sample_feedback_data['Nome'] in feedback_msg, "Nome feedback mancante"
        assert '[TEST]' in main_msg and '[TEST]' in area_msg and '[TEST]' in feedback_msg, "Marker [TEST] mancante"
        
        print(f"\n✅ Tutti i messaggi formattati correttamente con dati da fixture!")
        print(f"� Training IT: {sample_training_data['Nome']} ({sample_training_data['Area']})")
        print(f"� Training HR: {alternative_training_data['Nome']} ({alternative_training_data['Area']})")
        print(f"� Feedback: {sample_feedback_data['Nome']} ({sample_feedback_data['Area']})")
    

# Test marker personalizzati per pytest
pytestmark = [
    pytest.mark.integration,  # Tutti questi sono test integration
    pytest.mark.asyncio       # Tutti richiedono asyncio
]