# Formazing - AI Coding Agent Instructions

## 🎯 Project Overview
**Formazing** is a Flask-based training management system that automates notifications via Telegram Bot and integrates with Notion as the primary database. The app uses Microsoft Graph API for email/calendar operations. It follows a "manual trigger, automatic execution" philosophy: no automatic actions, all operations require explicit user confirmation.

## 🏗️ Architecture Patterns

### Modular Service Architecture
The project follows a **facade pattern with specialized modules** for separation of concerns:

```
Flask Routes (routes.py)
    ↓
Training Service Orchestrator (training_service.py)
    ↓
├── NotionService (app/services/notion/) - 6 modules with facade pattern
├── TelegramService (telegram_service.py) - Orchestrates bot + commands + formatters  
└── Microsoft Graph Service (mgraph_service.py) - Teams/Email integration
```

**Key principle**: Each service is a facade that delegates to specialized submodules. Example: `NotionService` delegates query building to `QueryBuilder`, parsing to `DataParser`, CRUD to `CrudOperations`.

### Notion Service - Critical Architecture
The Notion integration was **refactored from a 540-line monolith to 6 specialized modules** (~150 lines each):

- `notion_client.py` - Core authentication & configuration  
- `query_builder.py` - Constructs Notion API queries for different filters
- `data_parser.py` - Converts Notion responses to internal format
- `crud_operations.py` - Database write operations (update status, batch ops)
- `diagnostics.py` - Health checks, validation, monitoring
- `__init__.py` - **Facade** providing backward-compatible unified API

**Pattern**: Dependency Injection - `NotionClient` is injected into modules that need it (`CrudOperations`, `Diagnostics`).

### Telegram Bot Architecture  
Three-component system with **clear separation of responsibilities**:

- `telegram_service.py` - **Orchestrator**: lifecycle, message sending, error handling
- `bot/telegram_commands.py` - **Command handlers**: `/oggi`, `/domani`, `/settimana` logic
- `bot/telegram_formatters.py` - **Formatting**: YAML-based templates with variable interpolation

**Configuration-driven**: Template messages in `config/message_templates.yaml`, group mappings in `config/telegram_groups.json`.

## 🔄 Async-First Architecture
**Flask routes are async** using native Flask async support (not using asyncio wrappers). Example:

```python
@main.route('/dashboard')
@auth.login_required
async def dashboard():
    # Use asyncio.gather() for parallel Notion API calls
    results = await asyncio.gather(
        notion_service.get_formazioni_by_status('Programmata'),
        notion_service.get_formazioni_by_status('Calendarizzata'),
        notion_service.get_formazioni_by_status('Conclusa'),
        return_exceptions=True
    )
```

**Key pattern**: Use `asyncio.gather()` for parallel API calls to Notion/Telegram to boost performance.

## 📊 Data Model & Workflow

### Notion Database Schema (Required Fields)
| Field | Type | Purpose |
|-------|------|---------|
| Nome | title | Training name |
| Area | multi_select | Target audience (IT, HR, R&D, etc.) |
| Data | date | Scheduled date/time |
| Stato | status | **Workflow state**: `Programmata` → `Calendarizzata` → `Conclusa` |
| Periodo | select | Training period: SPRING, AUTUMN, ONCE, EXT, OUT |
| Codice | rich_text | Auto-generated unique code (e.g., `IT-Security-2024-SPRING-01`) |
| Link Teams | url | Microsoft Teams meeting link |

### State Machine Workflow
```
1. User creates training in Notion → Status: "Programmata"
2. User triggers notification via Flask UI → App generates Codice, creates Teams meeting, sends Telegram/Email → Status: "Calendarizzata"  
3. After training completion, user sends feedback request → Status: "Conclusa"
```

**Critical**: The app NEVER auto-updates status without explicit user action in the UI.

## 🧪 Testing Strategy

### Test Organization (106 tests, ~1.2s execution)
```
tests/
├── conftest.py - Minimal global fixtures (event loop, env loading)
├── fixtures/ - 39 modular fixtures in 6 specialized files
│   ├── notion_fixtures.py - 8 base Notion fixtures
│   ├── query_builder_fixtures.py - 6 query construction fixtures  
│   ├── crud_fixtures.py - 8 CRUD operation fixtures
│   ├── client_fixtures.py - 7 auth/environment fixtures
│   ├── telegram_fixtures.py - 5 bot/training fixtures
│   └── facade_fixtures.py - 4 integration fixtures
├── unit/ - Fast tests, zero external dependencies
│   ├── notion/ - 86 tests for all 5 NotionService modules
│   └── test_telegram_formatter.py - 20 tests for message formatting
└── integration/ - Real Telegram bot tests (marked with @pytest.mark.real_telegram)
```

### Quick Test Commands (Windows)
```powershell
# Development: Run all unit tests (1.2s)
.\quick_test.bat unit

# Notion-specific tests only (0.9s)  
.\quick_test.bat notion

# Safe preview tests (no real messages)
.\quick_test.bat format

# Interactive test with confirmations (recommended before deploy)
.\quick_test.bat interactive

# Real Telegram tests (sends actual messages - use with caution!)
.\quick_test.bat training  # Test training notification
.\quick_test.bat feedback  # Test feedback request
.\quick_test.bat bot       # Test bot commands (60s)
```

**Pattern**: Run `unit` continuously during development, `interactive` before commits, `real` only for final validation.

### Fixture Design Philosophy
**Before refactor**: Single 900-line `conftest.py` with all fixtures.  
**After refactor**: Modular fixtures split by domain (Notion, Telegram, CRUD, etc.) with clear naming conventions:

- `mock_*` - Mock objects for unit tests
- `sample_*` - Sample data for testing
- `real_*` - Real service instances (for integration tests)

**Example**: `sample_formazione_data` provides consistent test data for all Notion parsing tests.

## 🔧 Development Workflows

### Adding a New Notion Query Filter
1. Add query builder method in `app/services/notion/query_builder.py` (e.g., `build_period_filter_query`)
2. Add facade method in `app/services/notion/__init__.py` that delegates to builder + parser
3. Add fixture in `tests/fixtures/query_builder_fixtures.py` 
4. Add unit tests in `tests/unit/notion/test_query_builder.py`
5. Run `.\quick_test.bat notion` to validate

### Adding a New Telegram Command
1. Add handler method in `app/services/bot/telegram_commands.py` (e.g., `handle_mese`)
2. Register handler in `telegram_service._initialize_bot()`: `CommandHandler("mese", self.commands.handle_mese)`
3. Update help text in `handle_help()`
4. Test interactively: `.\quick_test.bat bot` (sends real messages)

### Adding a New Flask Route
1. Add async route in `app/routes.py` with `@auth.login_required` decorator
2. Use `asyncio.gather()` if making multiple Notion calls
3. Return JSON for API routes, render template for HTML pages
4. Always include try/except with `NotionServiceError` handling

## 🚨 Common Pitfalls & Solutions

### Problem: Notion API Rate Limiting
**Solution**: Use `asyncio.gather()` to parallelize independent queries instead of sequential calls. Example in `routes.py::dashboard()`.

### Problem: Telegram Message Formatting Breaks  
**Solution**: Always use `telegram_formatters.py` methods - they handle Markdown escaping. Never construct messages manually with string concatenation.

### Problem: Test Fixtures Not Found
**Solution**: Import fixtures from `tests/fixtures/__init__.py` (auto-imports all). Check `conftest.py` has `from tests.fixtures import *`.

### Problem: Async Function Not Awaited
**Solution**: All Notion/Telegram operations are async. In Flask routes, use `await`. In pytest, mark tests with `@pytest.mark.asyncio` (or use `asyncio_mode = auto` in `pytest.ini`).

### Problem: Environment Variables Not Loading
**Solution**: Ensure `.env` file exists in project root. Use `Config.validate_config()` to check required vars: `TELEGRAM_BOT_TOKEN`, `NOTION_TOKEN`, `NOTION_DATABASE_ID`.

## 📝 Code Style Conventions

### Logging Pattern
```python
import logging
logger = logging.getLogger(__name__)

# Always log with context
logger.info(f"Dashboard loaded with {stats['totale']} trainings")
logger.error(f"NotionService error: {e}")
```

### Error Handling Pattern
```python
try:
    result = await notion_service.get_formazioni_by_status(status)
except NotionServiceError as e:
    logger.error(f"Notion error: {e}")
    flash(f"❌ Error: {e}", 'error')
    return redirect(url_for('main.home'))
except Exception as e:
    logger.error(f"Unexpected error: {e}")
    return jsonify({'error': str(e), 'status': 'error'}), 500
```

### Async Service Call Pattern
```python
# ✅ Good: Parallel calls with gather
results = await asyncio.gather(
    service.operation1(),
    service.operation2(),
    return_exceptions=True  # Continue even if one fails
)

# ❌ Bad: Sequential calls
result1 = await service.operation1()
result2 = await service.operation2()  # Wastes time waiting
```

### Query Builder Delegation Pattern
```python
# In NotionService facade (__init__.py)
async def get_formazioni_by_status(self, status: str) -> List[Dict]:
    """Facade method that orchestrates submodules."""
    query = self.query_builder.build_status_filter_query(status, self.client.get_database_id())
    response = self.client.get_client().databases.query(**query)
    return self.data_parser.parse_formazioni_list(response)
```

## 🔍 Key Files Reference

### Configuration
- `config.py` - Centralized config with `validate_config()` method
- `config/telegram_groups.json` - Area → Chat ID mapping
- `config/message_templates.yaml` - Telegram message templates
- `.env` - Secrets (not in repo, see `.env.example`)

### Services (Business Logic)
- `app/services/notion/__init__.py` - NotionService facade (entry point)
- `app/services/telegram_service.py` - Telegram orchestrator
- `app/services/mgraph_service.py` - Microsoft Graph integration
- `app/services/training_service.py` - Main orchestrator (coordinates all services)

### Web Layer
- `run.py` - Application entry point
- `app/__init__.py` - Flask app factory with Basic Auth setup
- `app/routes.py` - All Flask routes (async, uses `@auth.login_required`)

### Testing
- `pytest.ini` - Pytest config with asyncio mode, markers, logging
- `tests/conftest.py` - Global fixtures (minimal, most are in `fixtures/`)
- `tests/fixtures/*.py` - 39 modular fixtures organized by domain
- `quick_test.bat` - Fast test runner script with safety levels

### Documentation
- `README.md` - User guide, workflow explanation, testing matrix
- `docs/notion-service.md` - Deep dive on NotionService modular architecture
- `docs/bot-telegram.md` - Telegram bot architecture, commands, flows
- `docs/testing/` - Testing strategy, fixture guide, test workflows

## 🚀 Quick Start for New Contributors

1. **Setup environment**: `pip install -r requirements.txt` + create `.env` with required tokens
2. **Validate setup**: `.\quick_test.bat check` 
3. **Run unit tests**: `.\quick_test.bat unit` (should pass 106 tests in ~1.2s)
4. **Start Flask app**: `python run.py` (opens on http://localhost:5000)
5. **Check dashboard**: Login with credentials from `config.py` (Basic Auth)

## 📚 Further Reading
- **Notion Service Architecture**: `docs/notion-service.md` - Explains the 6-module refactor
- **Telegram Bot System**: `docs/bot-telegram.md` - Commands, formatting, message flows  
- **Testing Guide**: `docs/testing/fixture-testing-guide.md` - Complete fixture system reference
- **Fixture Quick Reference**: `docs/testing/fixture-quick-reference.md` - All 39 fixtures at a glance

---
*Last updated: Generated from codebase analysis on 2025-10-01*
