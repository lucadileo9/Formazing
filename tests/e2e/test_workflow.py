#!/usr/bin/env python3
"""
Test workflow completo Notion → Telegram
========================================

Questo script simula l'intero workflow di produzione:
1. 📊 Recupera formazioni da Notion
2. 🎨 Formatta messaggi con template
3. 🚀 Simula invio (SAFE MODE - nessun messaggio reale)
4. 📈 Verifica risultati e genera report
5. 🔍 Analizza performance e possibili problemi

Modalità:
- SAFE MODE: Non invia messaggi reali (default)
- REAL MODE: Invia messaggi veri (richiede conferma esplicita)

Usage: 
  python test_workflow.py                    # Safe mode
  python test_workflow.py --real             # Real mode (pericoloso!)
"""

import asyncio
import logging
import sys
import argparse
import time
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass

# Aggiungi la directory root del progetto al path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from app.services.notion import NotionService
from app.services.telegram_service import TelegramService
from app.services.bot.telegram_formatters import TelegramFormatter
from config import Config

# Configura logging per output pulito
logging.basicConfig(
    level=logging.WARNING,
    format='%(levelname)s: %(message)s'
)

@dataclass
class WorkflowResult:
    """Represents the final result of a workflow execution.

    Attributes:
        formazione_nome (str): The name of the training course associated with the workflow.
        formazione_id (str): The unique identifier for the training course.
        status (str): The final status of the workflow (e.g., 'completed', 'failed').
        groups_targeted (List[str]): A list of the group names targeted by the workflow.
        messages_generated (int): The total number of messages generated during the workflow.
        messages_sent (int): The number of messages that were successfully sent.
        success_rate (float): The percentage of messages that were sent successfully.
        execution_time (float): The total time in seconds the workflow took to complete.
        errors (List[str]): A list of error messages encountered during execution.
    """
    formazione_nome: str
    formazione_id: str
    status: str
    groups_targeted: List[str]
    messages_generated: int
    messages_sent: int
    success_rate: float
    execution_time: float
    errors: List[str]

class WorkflowTester:
    """Classe per testare il workflow completo"""
    
    def __init__(self, safe_mode: bool = True):
        self.safe_mode = safe_mode
        self.notion_service = None
        self.telegram_service = None
        self.formatter = None
        self.results: List[WorkflowResult] = []
        
    async def initialize_services(self) -> bool:
        """Inizializza tutti i servizi necessari"""
        print("🔧 Inizializzazione servizi...")
        
        try:
            # 1. NotionService
            self.notion_service = NotionService()
            print("✅ NotionService inizializzato")
            
            # 2. TelegramService (con NotionService iniettato)
            self.telegram_service = TelegramService(
                token=Config.TELEGRAM_BOT_TOKEN,
                notion_service=self.notion_service,  # ✅ Passa NotionService
                groups_config_path=Config.TELEGRAM_GROUPS_CONFIG,
                templates_config_path=Config.TELEGRAM_TEMPLATES_CONFIG
            )
            print("✅ TelegramService inizializzato")
            
            # 3. TelegramFormatter
            import yaml
            templates_path = project_root / "config" / "message_templates.yaml"
            with open(templates_path, 'r', encoding='utf-8') as f:
                templates = yaml.safe_load(f)
            self.formatter = TelegramFormatter(templates=templates)
            print("✅ TelegramFormatter inizializzato")
            
            return True
            
        except Exception as e:
            print(f"❌ Errore inizializzazione: {e}")
            return False
    
    async def get_test_formazioni(self, limit_per_status: int = 3) -> Dict[str, List[Dict]]:
        """Recupera formazioni di test per ogni status"""
        print(f"📊 Recupero max {limit_per_status} formazioni per status...")
        
        formazioni_by_status = {}
        statuses = ['Programmata', 'Calendarizzata', 'Conclusa']
        
        for status in statuses:
            try:
                all_formazioni = await self.notion_service.get_formazioni_by_status(status)
                # Limita numero per test più veloce
                formazioni = all_formazioni[:limit_per_status]
                
                if formazioni:
                    formazioni_by_status[status] = formazioni
                    print(f"✅ {status}: {len(formazioni)} formazioni (di {len(all_formazioni)} totali)")
                else:
                    print(f"⚠️ {status}: Nessuna formazione trovata")
                    
            except Exception as e:
                print(f"❌ Errore recupero {status}: {e}")
        
        return formazioni_by_status
    
    async def process_single_formazione(self, formazione: Dict) -> WorkflowResult:
        """Processes a single training event through the notification workflow.
        This asynchronous method orchestrates the entire process for one 'formazione'
        record. It determines the target audience, generates tailored messages,
        and sends them via Telegram. The operation can be run in a "safe mode"
        to simulate sending without actual API calls.
        The workflow consists of the following steps:
        1.  Determine Target Groups: Identifies which Telegram groups should be
            notified based on the training data.
        2.  Generate Messages: Formats a specific message for each target group.
        3.  Send Messages: Dispatches the generated messages. If `self.safe_mode`
            is True, this step is simulated. Otherwise, messages are sent for real.
        All errors encountered during formatting or sending are collected and
        included in the final result.
        Args:
            formazione (Dict): A dictionary representing a single training event,
                typically fetched from Notion. Expected to contain keys like
                'Nome', '_notion_id', and 'Stato'.
        Returns:
            WorkflowResult: A data object containing a comprehensive summary of the
                operation's outcome, including the number of messages generated and
                sent, success rate, execution time, and a list of errors.
        """
        start_time = time.time()
        
        nome = formazione.get('Nome', 'N/A')
        formazione_id = formazione.get('_notion_id', 'unknown')
        status = formazione.get('Stato', 'unknown')
        
        errors = []
        groups_targeted = []
        messages_generated = 0
        messages_sent = 0
        
        try:
            # 1. Determina gruppi target
            groups_targeted = self.telegram_service._get_target_groups(formazione)
            
            # 2. Genera messaggi
            messages = {}
            for group_key in groups_targeted:
                try:
                    message = self.formatter.format_training_message(
                        training_data=formazione,
                        group_key=group_key
                    )
                    messages[group_key] = message
                    messages_generated += 1
                except Exception as e:
                    errors.append(f"Formattazione gruppo {group_key}: {e}")
            
            # 3. Invio messaggi (reale o simulato)
            if self.safe_mode:
                # Simulazione invio
                messages_sent = messages_generated
                print(f"   🔒 SAFE MODE: Simulati {messages_sent} invii per '{nome}'")
            else:
                # Invio reale
                for group_key, message in messages.items():
                    try:
                        success = await self.telegram_service.send_message_to_group(
                            group_key=group_key,
                            message=message,
                            parse_mode='HTML'
                        )
                        if success:
                            messages_sent += 1
                    except Exception as e:
                        errors.append(f"Invio gruppo {group_key}: {e}")
                        
                print(f"   📱 REAL MODE: {messages_sent}/{messages_generated} messaggi inviati per '{nome}'")
                        
        except Exception as e:
            errors.append(f"Errore generale workflow: {e}")
        
        execution_time = time.time() - start_time
        success_rate = (messages_sent / messages_generated * 100) if messages_generated > 0 else 0
        
        return WorkflowResult(
            formazione_nome=nome,
            formazione_id=formazione_id,
            status=status,
            groups_targeted=groups_targeted,
            messages_generated=messages_generated,
            messages_sent=messages_sent,
            success_rate=success_rate,
            execution_time=execution_time,
            errors=errors
        )
    
    async def run_workflow_tests(self, formazioni_by_status: Dict[str, List[Dict]]) -> List[WorkflowResult]:
        """Esegue test workflow su tutte le formazioni"""
        print("🚀 Esecuzione workflow tests...")
        
        total_formazioni = sum(len(formazioni) for formazioni in formazioni_by_status.values())
        print(f"📈 Processando {total_formazioni} formazioni...")
        
        results = []
        current = 0
        
        for status, formazioni in formazioni_by_status.items():
            print(f"\n📋 Processando formazioni '{status}':")
            
            for formazione in formazioni:
                current += 1
                nome = formazione.get('Nome', f'Formazione #{current}')
                print(f"   {current:2d}/{total_formazioni} - {nome[:50]}...")
                
                try:
                    result = await self.process_single_formazione(formazione)
                    results.append(result)
                    
                    # Status rapido
                    if result.success_rate == 100:
                        print(f"      ✅ 100% ({result.messages_sent} messaggi)")
                    elif result.success_rate > 0:
                        print(f"      ⚠️ {result.success_rate:.1f}% ({result.messages_sent}/{result.messages_generated})")
                    else:
                        print(f"      ❌ 0% (falliti tutti)")
                        
                except Exception as e:
                    print(f"      💥 Errore critico: {e}")
                    # Crea risultato di errore
                    error_result = WorkflowResult(
                        formazione_nome=nome,
                        formazione_id='error',
                        status=status,
                        groups_targeted=[],
                        messages_generated=0,
                        messages_sent=0,
                        success_rate=0,
                        execution_time=0,
                        errors=[str(e)]
                    )
                    results.append(error_result)
        
        return results
    
    def generate_report(self, results: List[WorkflowResult]) -> None:
        """Genera report dettagliato dei risultati"""
        print("\n" + "=" * 80)
        print("📊 REPORT WORKFLOW COMPLETO")
        print("=" * 80)
        
        if not results:
            print("❌ Nessun risultato da analizzare")
            return
        
        # Statistiche generali
        total_formazioni = len(results)
        total_messages_generated = sum(r.messages_generated for r in results)
        total_messages_sent = sum(r.messages_sent for r in results)
        
        successi_completi = sum(1 for r in results if r.success_rate == 100)
        successi_parziali = sum(1 for r in results if 0 < r.success_rate < 100)
        fallimenti = sum(1 for r in results if r.success_rate == 0)
        
        avg_execution_time = sum(r.execution_time for r in results) / total_formazioni
        overall_success_rate = (total_messages_sent / total_messages_generated * 100) if total_messages_generated > 0 else 0
        
        print(f"📈 STATISTICHE GENERALI:")
        print(f"   📚 Formazioni processate: {total_formazioni}")
        print(f"   📨 Messaggi generati: {total_messages_generated}")
        print(f"   ✅ Messaggi inviati: {total_messages_sent}")
        print(f"   🎯 Success rate globale: {overall_success_rate:.1f}%")
        print(f"   ⏱️ Tempo medio per formazione: {avg_execution_time:.2f}s")
        
        print(f"\n📊 DISTRIBUZIONE RISULTATI:")
        print(f"   ✅ Successi completi (100%): {successi_completi} ({successi_completi/total_formazioni*100:.1f}%)")
        print(f"   ⚠️ Successi parziali (1-99%): {successi_parziali} ({successi_parziali/total_formazioni*100:.1f}%)")
        print(f"   ❌ Fallimenti (0%): {fallimenti} ({fallimenti/total_formazioni*100:.1f}%)")
        
        # Analisi per status
        print(f"\n📋 ANALISI PER STATUS:")
        status_stats = {}
        for result in results:
            status = result.status
            if status not in status_stats:
                status_stats[status] = {'count': 0, 'success_rate': 0, 'total_rate': 0}
            status_stats[status]['count'] += 1
            status_stats[status]['total_rate'] += result.success_rate
        
        for status, stats in status_stats.items():
            avg_rate = stats['total_rate'] / stats['count']
            print(f"   📌 {status}: {stats['count']} formazioni, {avg_rate:.1f}% success rate medio")
                
        # Problemi
        print(f"\n⚠️ PROBLEMI RISCONTRATI:")
        all_errors = []
        for result in results:
            all_errors.extend(result.errors)
        
        if all_errors:
            # Raggruppa errori simili
            error_counts = {}
            for error in all_errors:
                error_type = error.split(':')[0] if ':' in error else error
                error_counts[error_type] = error_counts.get(error_type, 0) + 1
            
            for error_type, count in sorted(error_counts.items(), key=lambda x: x[1], reverse=True):
                print(f"   ❌ {error_type}: {count} occorrenze")
        else:
            print("   ✅ Nessun errore riscontrato!")
        
async def main():
    """Esegue il test workflow completo"""
    parser = argparse.ArgumentParser(description='Test workflow completo Notion → Telegram')
    parser.add_argument('--real', action='store_true', help='Modalità REAL (invia messaggi veri)')
    parser.add_argument('--limit', type=int, default=3, help='Limite formazioni per status (default: 3)')
    args = parser.parse_args()
    
    safe_mode = not args.real
    
    print("🔄 FORMAZING - Test Workflow Completo")
    print("=" * 60)
    
    if safe_mode:
        print("🔒 MODALITÀ SAFE: Nessun messaggio reale verrà inviato")
    else:
        print("⚠️ MODALITÀ REAL: Verranno inviati messaggi veri!")
        
        # Conferma per modalità real
        conferma = input("❓ Conferma modalità REAL (digitare 'CONFERMO'): ")
        if conferma != 'CONFERMO':
            print("❌ Modalità REAL non confermata, passa a SAFE mode")
            safe_mode = True
    
    try:
        # 1. Inizializza tester
        tester = WorkflowTester(safe_mode=safe_mode)
        
        # 2. Inizializza servizi
        if not await tester.initialize_services():
            print("❌ Inizializzazione servizi fallita")
            return False
        
        # 3. Recupera formazioni di test
        formazioni_by_status = await tester.get_test_formazioni(limit_per_status=args.limit)
        if not formazioni_by_status:
            print("❌ Nessuna formazione disponibile per test")
            return False
        
        # 4. Esegui workflow tests
        results = await tester.run_workflow_tests(formazioni_by_status)
        
        # 5. Genera report
        tester.generate_report(results)
        
        # 6. Risultato finale
        if results:
            overall_success = sum(r.success_rate for r in results) / len(results)
            success = overall_success >= 80  # Soglia di successo
            
            print(f"\n🏁 RISULTATO FINALE: {'✅ SUCCESSO' if success else '❌ PROBLEMI RILEVATI'}")
            return success
        else:
            print("\n❌ Nessun risultato ottenuto")
            return False
            
    except KeyboardInterrupt:
        print("\n⏹️ Test interrotto dall'utente")
        return False
    except Exception as e:
        print(f"\n💥 Errore imprevisto: {e}")
        return False

if __name__ == "__main__":
    try:
        result = asyncio.run(main())
        sys.exit(0 if result else 1)
    except Exception as e:
        print(f"\n💥 Errore critico: {e}")
        sys.exit(1)