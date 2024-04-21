# External dependencies
import datetime

# Internal dependencies
from src.file import File

class Directory:
    """
    Represents a directory.
    """
    
    # Constructor ------------------------------------------------------------------------
    
    def __init__(self, name: str, parent: "Directory" = None):
        """
        Args:
            name (str): Directory name
            parent (Directory, optional): Parent directory. Defaults to None.
        """
        
        self.name = name
        self.directory_childrens: list["Directory"] = list()
        self.file_childrens: list[File] = list()
        self.parent = parent
        
        self.creation_date = datetime.datetime.now()
        self.last_modified_date = self.creation_date
    
    
    # Methods --------------------------------------------------------------------------
    
    def add_child_directory(self, child_directory: "Directory") -> None:
        """
        Add a new child directory.

        Args:
            child (Directory): A child directory.
        """
        
        if not isinstance(child_directory, Directory):
            print("Child directory must be an instance of Directory")
            return
        
        if not self.check_directory_existence(child_directory.name):
            child_directory.parent = self
            self.directory_childrens.append(child_directory)
    
    
    def add_child_file(self, child_file: File) -> None:
        """
        Add a new child file.

        Args:
            child (File): A child file.
        """
        
        if not isinstance(child_file, File):
            print("Child file must be an instance of File")
            return
        
        if not self.check_file_existence(child_file.name):
            self.file_childrens.append(child_file)
    
            
    def check_existence(self, file_object_name: str):
        """
        Checks if a file object with the same name already exists in this directory.

        Args:
            file_object_name (str): Object name.

        Returns:
            bool: True if a object with the same name already exists, False if not.
        """
        
        for directory in self.directory_childrens:
            
            if (directory.name == file_object_name):
                return True
        
        for file in self.file_childrens:
            
            if (file.name == file_object_name):
                return True
        
        return False
    
    def check_directory_existence(self, dir_name: str):
        """
        Checks if a directory with the same name already exists in this directory.

        Args:
            dir_name (str): Directory name.

        Returns:
            bool: True if a directory with the same name already exists, False if not.
        """
        
        for directory in self.directory_childrens:
            
            if (directory.name == dir_name):
                return True

        return False
    
    def check_file_existence(self, file_name: str):
        """
        Checks if a file with the same name already exists in this directory.

        Args:
            file_name (str): File name.

        Returns:
            bool: True if a file with the same name already exists, False if not.
        """
        
        for file in self.file_childrens:
            
            if (file.name == file_name):
                return True
        
        return False

    def find_file(self, file_object_name: str):
        """
        Finds a child file.

        Args:
            file_name (str): File name

        Returns:
            Directory, File: returns a file object with the same name, and its type.
        """
        
        for file in self.file_childrens:
            if (file.name == file_object_name):
                return file
        
        return None
    
    def find_directory(self, dir_name: str):
        """
        Finds a child directory.

        Args:
            dir_name (str): Directory name

        Returns:
            Directory: returns a directory with the same name, and its type.
        """
        
        for directory in self.directory_childrens:
            if (directory.name == dir_name):
                return directory
        
        return None

    def find_objects(self, file_object_name: str):
        """
        Finds file objects with same name.

        Args:
            file_object_name (str): Object name

        Returns:
            list[File | Directory]: file objects with same name
        """
        objects = []
        
        for directory in self.directory_childrens:
            if (directory.name == file_object_name):
                objects.append(directory)
        
        for file in self.file_childrens:
            if (file.name == file_object_name):
                objects.append(file)
        
        return objects
    
    def find(self, file_object_name: str):
        """
        Finds a child directory or file.

        Args:
            file_object_name (str): Name of the file or directory to find.

        Returns:
            Directory, File: Returns the directory or file object with the same name, or None if not found.
        """
        
        # First check if it's a directory
        directory = self.find_directory(file_object_name)
        if directory:
            return directory
        
        # If not found, check if it's a file
        file = self.find_file(file_object_name)
        if file:
            return file
        
        # If not found, return None
        return None

    def modify_name(self, new_name: str):
        """
        Changes current directory name.

        Args:
            new_name (str): New directory name.
        """
        
        if not self.check_existence(new_name):
            self.name = new_name
            self.last_modified_date = datetime.datetime.now()
            return True

        return False
        
    def remove_child(self, file_object) -> bool:
        """
        Remove a child directory.

        Args:
            file_object (Directory | File): Name of the directory to be removed.
        """
        
        if (file_object != None):
            if (isinstance(file_object, Directory)):
                self.directory_childrens.remove(file_object)
            else:
                self.file_childrens.remove(file_object)
            return True
        
        return False
