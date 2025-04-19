"""
AI-Powered Terminal
A custom-built terminal that accepts both shell commands and natural language input.
"""

from .terminal import AITerminal
from .lexer import Lexer
from .parser import Parser
from .command_validator import CommandValidator
from .executor import CommandExecutor
from .ai_fallback import AIFallback

__version__ = '1.0.0'
__author__ = 'Hem Chandra Joshi, Himanshu Joshi, Mayank Joshi, Mayank Singh Negi'
