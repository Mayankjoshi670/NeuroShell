import os
from colorama import init, Fore
from typing import Optional

from lexer import Lexer
from parser import Parser
from command_validator import CommandValidator
from executor import CommandExecutor
from ai_fallback import AIFallback

# Initialize colorama for Windows color support
init()

class AITerminal:
    def __init__(self):
        self.lexer = Lexer()
        self.parser = Parser()
        self.validator = CommandValidator()
        self.executor = CommandExecutor()
        self.ai_fallback = AIFallback()

    def get_prompt_text(self) -> str:
        """Generate the prompt text with current directory."""
        cwd = os.getcwd()
        return f"{Fore.GREEN}> {Fore.BLUE}{cwd}{Fore.RESET} $ "

    def process_input(self, user_input: str) -> Optional[str]:
        """Process user input and return the result."""
        if not user_input.strip():
            return None

        # Check if it's a direct shell command
        if self.lexer.is_shell_command(user_input):
            tokens = [Token('IDENTIFIER', word) for word in user_input.split()]
        else:
            # Tokenize the natural language input
            tokens = self.lexer.tokenize(user_input)

        # Parse tokens into AST
        ast = self.parser.parse(tokens)
        if not ast:
            # Try AI fallback
            command = self.ai_fallback.get_command_suggestion(user_input)
            if command:
                print(f"{Fore.YELLOW}Suggested command: {command}{Fore.RESET}")
                user_confirm = input("Execute this command? [y/N]: ").lower()
                if user_confirm != 'y':
                    return None
                # Reprocess the suggested command
                return self.process_input(command)
            return f"{Fore.RED}Could not understand the command{Fore.RESET}"

        # Validate the command
        is_safe, error = self.validator.validate(ast)
        if not is_safe:
            return f"{Fore.RED}Error: {error}{Fore.RESET}"

        # Execute the command
        success, error = self.executor.execute(ast)
        if success:
            output = self.executor.get_last_output()
            return output if output else f"{Fore.GREEN}Command executed successfully{Fore.RESET}"
        else:
            return f"{Fore.RED}Error: {error}{Fore.RESET}"

    def run(self):
        """Run the terminal interface."""
        print(f"{Fore.CYAN}AI-Powered Terminal{Fore.RESET}")
        print(f"{Fore.CYAN}Type 'exit' to quit{Fore.RESET}")
        
        while True:
            try:
                # Get user input
                user_input = input(self.get_prompt_text())
                
                # Check for exit command
                if user_input.lower() in ['exit', 'quit']:
                    print(f"{Fore.YELLOW}Goodbye!{Fore.RESET}")
                    break
                
                # Process the input
                result = self.process_input(user_input)
                if result:
                    print(result)
                    
            except KeyboardInterrupt:
                continue
            except EOFError:
                break
            except Exception as e:
                print(f"{Fore.RED}Error: {str(e)}{Fore.RESET}")

if __name__ == '__main__':
    terminal = AITerminal()
    terminal.run()
