"""
Bot Telegram Module - Moduli specializzati per servizio Telegram

Struttura:
- telegram_formatters.py: Gestione template e formattazione messaggi
- telegram_commands.py: Comandi bot interattivi (/oggi, /domani, etc.)
"""

from .telegram_formatters import TelegramFormatter
from .telegram_commands import TelegramCommands

__all__ = ['TelegramFormatter', 'TelegramCommands']