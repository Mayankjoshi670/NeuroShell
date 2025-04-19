from typing import Dict, Any, Optional
from lexer import Token

class ASTNode:
    def __init__(self, type: str, value: Any = None):
        self.type = type
        self.value = value
        self.children = []

    def add_child(self, node: 'ASTNode'):
        self.children.append(node)

class Parser:
    def __init__(self):
        self.command_mappings = {
            'CREATE_DIRECTORY': 'mkdir',
            'DELETE': 'rm',
            'CHANGE_DIR': 'cd',
            'LIST_CONTENTS': 'ls'
        }

    def parse(self, tokens: list[Token]) -> Optional[ASTNode]:
        """Parse tokens into an AST."""
        if not tokens:
            return None

        # Handle direct shell commands
        if tokens[0].type == 'IDENTIFIER' and tokens[0].value in ['ls', 'cd', 'mkdir', 'rm']:
            command = ASTNode('SHELL_COMMAND', tokens[0].value)
            for token in tokens[1:]:
                command.add_child(ASTNode('ARGUMENT', token.value))
            return command

        # Handle natural language commands
        return self._parse_natural_language(tokens)

    def _parse_natural_language(self, tokens: list[Token]) -> Optional[ASTNode]:
        """Parse natural language commands into an AST."""
        i = 0
        root = None

        while i < len(tokens):
            token = tokens[i]

            if token.type == 'CREATE':
                root = self._parse_create_command(tokens[i:])
                break
            elif token.type == 'DELETE':
                root = self._parse_delete_command(tokens[i:])
                break
            elif token.type == 'CHANGE_DIR':
                root = self._parse_cd_command(tokens[i:])
                break
            elif token.type == 'LIST':
                root = self._parse_list_command(tokens[i:])
                break

            i += 1

        return root

    def _parse_create_command(self, tokens: list[Token]) -> ASTNode:
        """Parse create directory command."""
        root = ASTNode('COMMAND', 'mkdir')
        
        for i, token in enumerate(tokens):
            if token.type in ['DIRECTORY', 'IDENTIFIER'] and i + 1 < len(tokens):
                if tokens[i + 1].type == 'IDENTIFIER':
                    root.add_child(ASTNode('ARGUMENT', tokens[i + 1].value))
                    break

        return root

    def _parse_delete_command(self, tokens: list[Token]) -> ASTNode:
        """Parse delete command."""
        root = ASTNode('COMMAND', 'rm')
        
        for token in tokens:
            if token.type in ['IDENTIFIER', 'PATH']:
                root.add_child(ASTNode('ARGUMENT', token.value))

        return root

    def _parse_cd_command(self, tokens: list[Token]) -> ASTNode:
        """Parse change directory command."""
        root = ASTNode('COMMAND', 'cd')
        
        for token in tokens:
            if token.type in ['IDENTIFIER', 'PATH']:
                root.add_child(ASTNode('ARGUMENT', token.value))
                break

        return root

    def _parse_list_command(self, tokens: list[Token]) -> ASTNode:
        """Parse list contents command."""
        root = ASTNode('COMMAND', 'ls')
        
        for token in tokens:
            if token.type in ['FLAG', 'PATH']:
                root.add_child(ASTNode('ARGUMENT', token.value))

        return root
