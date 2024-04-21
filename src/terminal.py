# Internal dependencies
from src.file import File
from src.directory import Directory
from src.interface import Interface

# Terminal colors
RED = '\033[91m'
GREEN = '\033[92m'
BLUE = '\033[94m'
RESET = '\033[0m'


class Terminal:
    
    
    def __init__(self, root_directory: Directory) -> None:
        
        self.root_directory = root_directory
        self.current_directory = root_directory
        self.path = ""
        self.last_path = ""
        
        self.commands = {
            "ls": self.command_ls,
            "cd": self.command_cd,
            "pwd": self.command_pwd,
            "mkdir": self.command_mkdir,
            "touch": self.command_touch,
            "rm": self.command_rm,
            "rename": self.command_rename,
            "mv": self.command_mv,
            "clear": self.command_clear,
            "nano": self.command_nano,
            "cat": self.command_cat,
            "interface": self.command_interface,
            "exit": self.command_exit,
            "help": self.command_help
        }
        
    
    """
    Command functions
    """
    
    def command_exit(self, terminal_input: list[str]):
        """
        Exits from simulation.

        Args:
            terminal_input (list[str]): commands from user input
        """
        
        # Checking if there are too many arguments
        if (len(terminal_input) > 0):
            print(f"exit: too many arguments")
            return
        
        resp = str(input("Want to stop running? (y/n): ")).lower()
        if (resp == "y"):
            exit(1)
        elif (resp != "n"):
            self.command_exit(terminal_input)


    def command_ls(self, terminal_input: list[str]):
        """
        Simulates 'ls' terminal command.

        Args:
            terminal_input (list[str]): commands from user input
        """
        
        #TODO: Filipe e Elias - colocar argumentos '-r', '-t', '-a' (o '-a' seria legal a gnt botar pros arquivos que começam com '.' não aparecerem quando da o ls normal, só com 'ls -a')

        file_objects = []
        
        for file in self.current_directory.file_childrens: 
            file_objects.append(file)
            
        for directory in self.current_directory.directory_childrens:    
            file_objects.append(directory)
        
        file_objects = sorted(file_objects, key=lambda x: x.name)
        
        if len(file_objects) == 0:
            return
        
        for file_object in file_objects:
            if not file_object.name.startswith("."): #verifica se comeca com " . "
                if (isinstance(file_object, Directory)):
                    print(BLUE + f"{file_object.name} " + RESET, end=" ")
                else:
                    print(f"{file_object.name} ", end=" ")
                
        print("")
                

    def command_cd(self, terminal_input: list[str]):
        """
        Simulates 'cd' terminal command.

        Args:
            terminal_input (list[str]): commands from user input
        """
        
        # Checking if there are too many arguments
        if (len(terminal_input) > 1):
            print(f"cd: invalid arguments")
            return
        
        # Going to root directory
        elif (len(terminal_input) == 0):
            self.go_to_root()
            return
        
        # Saving navigation state
        last_directory = self.current_directory
        last_path = self.path
        
        # Checking if the command intends to navigate from the root folder
        if terminal_input[0][0] == "/":
            self.go_to_root()

        # Spliting string to get directories and filtering empty strings
        directories = []
        for directory_name in terminal_input[0].split("/"):
            if directory_name:
                directories.append(directory_name)
        
        # Executing commands
        for directory_name in directories:
            
            # Going back
            if directory_name == "..":
                if self.current_directory.parent == None:
                    print(f"cd: Cannot access any folders prior to the root directory")
                    return
                self.current_directory = self.current_directory.parent
                self.update_path_to(self.path.rsplit("/", 1)[0])

            # Returning to last path
            elif directory_name == "-":
                if len(directories) > 1:
                    print(f"cd: No such file or directory: {terminal_input[0]}")
                
                else:
                    self.update_path_to(self.last_path)
            
            # Going forward
            elif self.current_directory.check_directory_existence(directory_name):
                self.current_directory = self.current_directory.find_directory(directory_name)
                self.update_path_to(self.path + f"/{directory_name}")
            
            # Treating the non-existence of the directory
            else:
                if self.current_directory.check_file_existence(directory_name):
                    print(f"cd: not a directory: {terminal_input[0]}")
                else:
                    print(f"cd: no such file or directory: {terminal_input[0]}")
                    
                # Restoring the original navigation state

                self.current_directory = last_directory
                self.path = last_path
    

    def command_pwd(self, terminal_input: list[str]):
        """
        Simulates 'pwd' terminal command.


        Args:
            terminal_input (list[str]): commands from user input
        """
        
        # Checking if there are too many arguments
        if (len(terminal_input) > 0):
            print(f"pwd: too many arguments")
            return
        
        path = "/" if self.path == "" else self.path
        
        print(path)
       

    def command_mkdir(self, terminal_input: list[str]):
        """
        Simulates 'mkdir' terminal command.


        Args:
            terminal_input (list[str]): commands from user input
        """
        
        # Checking if there are wrong arguments
        for command in terminal_input:
            if command[0] == '-':
                print(f"mkdir: invalid option -- '{command[1:]}'")
                return
        
        # Creating directories
        for command in terminal_input:
            if (self.current_directory.check_existence(command)):
                print(f"mkdir: cannot create directory ‘{command}’: File exists")
                return
            
            self.current_directory.add_child_directory(Directory(command, self.current_directory))
      
                
    def command_touch(self, terminal_input: list[str]):
        """
        Simulates 'touch' terminal command.


        Args:
            terminal_input (list[str]): commands from user input
        """
        
        # Checking if there are too many arguments
        if (len(terminal_input) < 1):
            print(f"touch: invalid arguments")
            return

        # Creating file
        for name in terminal_input:
            if not self.current_directory.check_existence(name):
                new_file = File(self.current_directory, name)
                self.current_directory.add_child_file(new_file)
       
        
    def command_rm(self, terminal_input: list[str]):
        """
        Simulates 'rm' terminal command to remove file or directory

        Args: 
            terminal_input (list[str]): commands from user input
        """
        
        # Checking for extra arguments
        can_remove_dir = False
        
        if len(terminal_input) < 1:
            print(f"touch: invalid arguments")
            return
        
        elif "-r" in terminal_input:
            can_remove_dir = True
            terminal_input = [name for name in terminal_input if name != "-r"]
        
        for name in terminal_input:
            file_objects = self.current_directory.find_objects(name)
            if (len(file_objects) == 0):
                print(f"rm: cannot remove '{name}': No such file or directory")
            else:
                for file_object in file_objects:
                    if (isinstance(file_object, Directory) and not can_remove_dir):
                        print(f"rm: cannot remove '{file_object.name}': Is a directory")
                        print("use '-r' flag to remove directories too")
                    else:
                        self.current_directory.remove_child(file_object)

    def command_mv(self, terminal_input: list[str]):
        """
        Rename or move file 

        Args:
            terminal_input (list[str]): list from the terminal containing the command arguments

        Returns:
            None
        """

        # Checking if there are too many arguments
        if len(terminal_input) != 2:
            print("Use: mv <current_name> <new_name)")
            return

        # Extract source and destination from arguments
        source_name, destination_name = terminal_input

        # Find object to be renamed/moved
        to_move_object = None

        for object in self.current_directory.directory_childrens + self.current_directory.file_childrens:
            if object.name == source_name:
                to_move_object = object
                break

        if to_move_object:
            # If object exists in the directory
            if isinstance(to_move_object, File):
                # Check if destination is an existing file
                destination_file = self.current_directory.find_file(destination_name)
                if destination_file:
                    # Rename file
                    if not self.current_directory.check_existence(destination_name):
                        to_move_object.modify_name(destination_name)
                    else:
                        print(f"You can't rename to '{destination_name}'. File already exists!")
                else:
                    # Check if destination is an existing directory
                    destination_directory = self.current_directory.find_directory(destination_name)
                    if destination_directory:
                        # Move to destination directory
                        self.current_directory.remove_child(to_move_object)
                        destination_directory.add_child_file(to_move_object)
                    else:
                        # Destination isn't valid directory
                        print(f"O destino '{destination_name}' não é um diretório válido!")
            elif isinstance(to_move_object, Directory):  # Added condition for checking if to_move_object is a directory
                # Check if destination is an existing directory
                destination_directory = self.current_directory.find_directory(destination_name)
                if destination_directory:
                    # Move to destination directory
                    self.current_directory.remove_child(to_move_object)
                    destination_directory.add_child_directory(to_move_object)
                else:
                    # Destination isn't valid directory
                    print(f"O destino '{destination_name}' não é um diretório válido!")
            else:
                # Object is not a file or directory
                print(f"O objeto '{source_name}' não é um arquivo ou diretório!")
        else:
            # Object isn't found in directory
            print(f"O objeto '{source_name}' não foi encontrado!")


    def command_rename(self, terminal_input: list[str]):
        """
        Renames a file or directory.

        Args:
            terminal_input (list[str]): List of input arguments from the terminal.

        Returns:
            None
        """

        # Checking if there are too few or too many arguments
        if len(terminal_input) != 2:
            print("Use: rename <current_name> <new_name>")
            return

        # Extract current and new names from arguments
        current_name, new_name = terminal_input

        # Find the object to be renamed
        to_rename_object = None

        for obj in self.current_directory.directory_childrens + self.current_directory.file_childrens:
            if obj.name == current_name:
                to_rename_object = obj
                break

        if to_rename_object:
            # Check if new name already exists
            if not self.current_directory.check_existence(new_name):
                # Rename the object
                to_rename_object.modify_name(new_name)
            else:
                print(f"You can't rename to '{new_name}'. File or directory already exists!")
        else:
            # Object not found in the directory
            print(f"Object '{current_name}' not found!")
                 
     
    
    def command_nano(self, terminal_input: list[str]):
        """
        Simulates 'nano' terminal command to edit file content

        Args:
            terminal_input (list[str]): commands from user input
        """
        
        # Checking for extra arguments
        if len(terminal_input) > 2:
            print(f"nano: too many arguments")
            print(f"try: nano <file_name> <content>")
            return
        
        elif len(terminal_input) == 0:
            print(f"nano: invalid arguments")
            print(f"try: nano <file_name> <content>")
            return
        
        # File name that will be edited
        file_name = terminal_input[0]
        
        # Check if file exists
        file = self.current_directory.find_file(file_name)
        if file:
            file.content = terminal_input[1]
        else:
            print(f"nano: '{file_name}' file not found")


    def command_cat(self, terminal_input: list[str]):
        """
        Simulates 'cat' terminal command to see file content

        Args:
            terminal_input (list[str]): commands from user input
        """
        
        if len(terminal_input) != 1:
            print(f"nano: invalid arguments")
            print(f"try: cat <file_name>")
            return
        
        # File name that will be edited
        file_name = terminal_input[0]
        
        # Check if file exists
        file = self.current_directory.find_file(file_name)
        if file:
            print(file.content)
        else:
            print(f"cat: '{file_name}' file not found")
        
        
    def command_clear(self, terminal_input:str):
        """
        Simulates 'clear' terminal command. 

        Args:
            terminal_input (list[str]): commands from user input
        """
        
        print("\033[H\033[J", end='')
 
 
    def command_interface(self, terminal_input: list[str]):
        """
        Shows file tree.

        Args:
            terminal_input (list[str]): commands from user input
        """
        
        # Checking if there are too many arguments
        if (len(terminal_input) > 0):
            print(f"interface: too many arguments")
            return
        
        print("interface: close the popped window to continue.")
        interface = Interface(self.root_directory)
        interface.display_tree()
         
    
    def command_help(self, terminal_input: list[str]):
        # Checking if there are too many arguments
        if (len(terminal_input) > 0):
            print(f"help: too many arguments")
            return

        print("--Commands: ")
        for command in self.commands.keys():
            print(command)
        
    """
    Utilitary functions
    """
    
    def get_input_command(self):
        """
        Collects user command.
        """
        path = "/" if self.path == "" else self.path
            
        return str(input(GREEN + "user@desktop" + RESET + ":" + BLUE + f"{path}" + RESET + "$ "))
    
    
    def update_path_to(self, new_path: str):
        """
        Updates the current path

        Args:
            new_path (str): path name
        """

        self.last_path = self.path
        self.path = new_path


    def interpret_command(self, terminal_input: list[str]):
        """
        Processes the command received from the user.

        Args:
            terminal_input (list[str]): string with user inputs
        """
        
        terminal_input = terminal_input.rstrip().split(" ")
        command = terminal_input[0]
        
        if command in self.commands:
            self.commands[command](terminal_input[1:])
            
        elif command != "":
            print(f"Command {command} not found.")
    
    def go_to_root(self):
        """
        Goes to root directory
        """
        
        self.current_directory = self.root_directory
        self.update_path_to("")
    