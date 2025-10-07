"""
Script di test veloce per Microsoft Service.

Verifica che:
1. La configurazione sia valida
2. I moduli si importino correttamente
3. Il servizio si inizializzi senza errori
"""

import sys
import os

# Aggiungi root al path (tests/unit -> tests -> root)
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from config import Config
from app.services.microsoft import MicrosoftService, MicrosoftServiceError


def test_config():
    """Testa la configurazione."""
    print("🔍 Testing configuration...")
    validation = Config.validate_config()
    
    print(f"  Telegram: {'✅' if validation['telegram'] else '❌'}")
    print(f"  Notion: {'✅' if validation['notion'] else '❌'}")
    print(f"  Microsoft Graph: {'✅' if validation['microsoft_graph'] else '❌'}")
    print(f"  Flask Auth: {'✅' if validation['flask_auth'] else '❌'}")
    
    if not validation['microsoft_graph']:
        print("\n⚠️  Microsoft Graph non configurato completamente.")
        print("   Variabili richieste in .env:")
        print("   - MICROSOFT_TENANT_ID")
        print("   - MICROSOFT_CLIENT_ID")
        print("   - MICROSOFT_CLIENT_SECRET")
        print("   - MICROSOFT_USER_EMAIL")
        return False
    
    return True


def test_service_initialization():
    """Testa l'inizializzazione del servizio."""
    print("\n🔧 Testing service initialization...")
    
    try:
        service = MicrosoftService()
        print("  ✅ MicrosoftService initialized")
        
        info = service.get_service_info()
        print(f"  User: {info['user_email']}")
        print(f"  Tenant: {info['tenant_id']}")
        print(f"  Template: {info['template_path']}")
        print(f"  Areas configured: {info['areas_configured']}")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False


def test_template_loading():
    """Testa il caricamento dei template."""
    print("\n📄 Testing template loading...")
    
    try:
        service = MicrosoftService()
        
        # Test formatting con dati sample
        sample_data = {
            'nome': 'Test Formazione',
            'codice': 'TEST-2024-01',
            'data': '2024-10-15T10:00:00Z',
            'area': 'IT'
        }
        
        subject = service.email_formatter.format_subject(sample_data)
        print(f"  ✅ Subject: {subject}")
        
        body = service.email_formatter.format_calendar_body(sample_data)
        print(f"  ✅ Body length: {len(body)} characters")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False


def main():
    """Esegue tutti i test."""
    print("=" * 60)
    print("🧪 Microsoft Service - Quick Test")
    print("=" * 60)
    
    results = []
    
    results.append(("Configuration", test_config()))
    results.append(("Service Init", test_service_initialization()))
    results.append(("Template Loading", test_template_loading()))
    
    print("\n" + "=" * 60)
    print("📊 RESULTS:")
    print("=" * 60)
    
    for name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"  {name}: {status}")
    
    all_passed = all(result[1] for result in results)
    
    print("\n" + "=" * 60)
    if all_passed:
        print("🎉 All tests passed!")
    else:
        print("⚠️  Some tests failed. Check configuration.")
    print("=" * 60)
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
