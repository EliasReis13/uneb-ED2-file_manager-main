# Internal dependencies
from src.terminal import Terminal
from src.directory import Directory

# Create user terminal
user_terminal = Terminal(Directory("root"))

if __name__ == "__main__":
    
    user_terminal.command_clear("")
    
    while(True):
    
        terminal_input = user_terminal.get_input_command()
        user_terminal.interpret_command(terminal_input)