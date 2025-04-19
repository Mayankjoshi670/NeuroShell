from typing import List, Dict

class Token:
    def __init__(self, type: str, value: str):
        self.type = type
        self.value = value

    def __str__(self):
        return f"Token({self.type}, {self.value})"

class Lexer:
    def __init__(self):
        self.keywords = {
            'create': 'CREATE',
            'make': 'CREATE',
            'new': 'CREATE',
            'folder': 'DIRECTORY',
            'directory': 'DIRECTORY',
            'named': 'NAMED',
            'called': 'NAMED',
            'delete': 'DELETE',
            'remove': 'DELETE',
            'go': 'CHANGE_DIR',
            'change': 'CHANGE_DIR',
            'to': 'TO',
            'list': 'LIST',
            'show': 'LIST',
            'contents': 'CONTENTS'
        }

    def tokenize(self, text: str) -> List[Token]:
        """Convert input text into a list of tokens."""
        words = text.lower().split()
        tokens = []
        
        i = 0
        while i < len(words):
            word = words[i]
            
            # Check if it's a keyword
            if word in self.keywords:
                tokens.append(Token(self.keywords[word], word))
            # Check if it's a path or filename
            elif '/' in word or '\\' in word:
                tokens.append(Token('PATH', word))
            # Check if it's a flag (starts with -)
            elif word.startswith('-'):
                tokens.append(Token('FLAG', word))
            # Otherwise treat as an identifier
            else:
                tokens.append(Token('IDENTIFIER', word))
            
            i += 1
            
        return tokens

    def is_shell_command(self, text: str) -> bool:
        """Check if the input appears to be a direct shell command."""
        common_commands = {'ls', 'cd', 'mkdir', 'rm', 'cp', 'mv', 'pwd', 'cat', 'echo'}
        first_word = text.strip().split()[0].lower()
        return first_word in common_commands
