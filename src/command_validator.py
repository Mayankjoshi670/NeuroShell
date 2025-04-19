import os
from typing import Tuple, Optional
from parser import ASTNode

class CommandValidator:
    def __init__(self):
        self.unsafe_commands = {
            'rm': {'rf', '-rf', '-r', 'f'},  # dangerous rm flags
            'sudo': set(),  # sudo is always unsafe
            ':(){:|:&};:': set(),  # fork bomb
        }
        
        self.allowed_commands = {
            'ls', 'cd', 'mkdir', 'rm', 'pwd', 'echo',
            'cat', 'cp', 'mv', 'touch'
        }

    def validate(self, ast: ASTNode) -> Tuple[bool, Optional[str]]:
        """
        Validate if the command is safe to execute.
        Returns (is_safe, error_message)
        """
        if not ast:
            return False, "Invalid command"

        command = ast.value.lower()
        
        # Check if command is allowed
        if command not in self.allowed_commands:
            return False, f"Command '{command}' is not allowed"

        # Check for unsafe flags or arguments
        if command in self.unsafe_commands:
            args = {child.value.lower() for child in ast.children}
            unsafe_args = args.intersection(self.unsafe_commands[command])
            if unsafe_args:
                return False, f"Unsafe arguments detected: {unsafe_args}"

        # Validate paths
        for child in ast.children:
            if child.type == 'ARGUMENT':
                path = child.value
                if '..' in path or '~' in path:
                    return False, "Path traversal not allowed"
                
                # Ensure path is within allowed directory
                abs_path = os.path.abspath(path)
                if not self._is_path_allowed(abs_path):
                    return False, "Path is outside allowed directory"

        return True, None

    def _is_path_allowed(self, path: str) -> bool:
        """Check if the path is within allowed directories."""
        # Get the current working directory as the base allowed path
        base_path = os.getcwd()
        
        # Normalize paths for comparison
        norm_path = os.path.normpath(path)
        norm_base = os.path.normpath(base_path)
        
        # Check if the path is a subdirectory of the base path
        return norm_path.startswith(norm_base)
