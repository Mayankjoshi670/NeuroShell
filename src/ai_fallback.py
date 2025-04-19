import os
from typing import Optional
import google.generativeai as genai
from dotenv import load_dotenv

class AIFallback:
    def __init__(self):
        load_dotenv()
        api_key = os.getenv('GOOGLE_API_KEY')
        if api_key:
            genai.configure(api_key=api_key)

        # Use the free-tier model
        self.model = genai.GenerativeModel('models/gemini-1.5-flash')

        self.command_templates = {
        "create directory": "mkdir {name}",
        "remove directory": "rmdir {name}",
        "change directory": "cd {path}",
        "list contents": "ls {path}",
        "copy file": "cp {source} {destination}",
        "move file": "mv {source} {destination}",
        "delete file": "rm {name}",
        "show file contents": "cat {name}",
    }


    def get_command_suggestion(self, user_input: str) -> Optional[str]:
        try:
            prompt = f"""
            Convert this natural language command to a shell command:
            "{user_input}"
            Only return the exact shell command, nothing else.
            Use common shell commands like: ls, cd, mkdir, rm, cp, mv, cat, echo.
            """
            response = self.model.generate_content(prompt)
            if response and response.text:
                command = response.text.strip().strip('`').strip()
                if self._is_valid_command(command):
                    return command
            return None
        except Exception as e:
            print(f"AI Fallback Error: {str(e)}")
            return None

    def _is_valid_command(self, command: str) -> bool:
        if not command:
            return False
        parts = command.split()
        if not parts:
            return False
        base_command = parts[0].lower()
        allowed_commands = {
            'ls', 'cd', 'mkdir', 'rmdir', 'rm', 'cp', 'mv',
            'cat', 'echo', 'touch', 'pwd'
        }
        if base_command not in allowed_commands:
            return False
        dangerous_patterns = [
            ';', '&&', '||', '|', '>', '>>', '<',
            'sudo', 'rm -rf', ':(){:|:&};:'
        ]
        return not any(pattern in command for pattern in dangerous_patterns)
