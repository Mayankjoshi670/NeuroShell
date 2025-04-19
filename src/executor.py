import subprocess
from typing import Tuple, Optional
from parser import ASTNode

class CommandExecutor:
    def __init__(self):
        self.last_output = ""
        self.last_error = ""

    def execute(self, ast: ASTNode) -> Tuple[bool, Optional[str]]:
        """
        Execute the command represented by the AST.
        Returns (success, error_message)
        """
        if not ast:
            return False, "Invalid command"

        command = [ast.value]
        for child in ast.children:
            if child.type == 'ARGUMENT':
                command.append(child.value)

        try:
            # Run the command and capture output
            process = subprocess.run(
                command,
                capture_output=True,
                text=True,
                shell=False  # More secure
            )

            self.last_output = process.stdout
            self.last_error = process.stderr

            if process.returncode == 0:
                return True, None
            else:
                return False, process.stderr

        except subprocess.SubprocessError as e:
            return False, str(e)
        except Exception as e:
            return False, f"Error executing command: {str(e)}"

    def get_last_output(self) -> str:
        """Get the output from the last executed command."""
        return self.last_output

    def get_last_error(self) -> str:
        """Get the error from the last executed command."""
        return self.last_error
