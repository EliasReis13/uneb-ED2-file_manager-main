# External dependencies
import datetime

class File:
    """
    Represents a file.
    """
    
    # Constructor ---------------------------------------------------------------
    
    def __init__(self, parent, name: str, content: str = None):
        """
        Args:
            name (str): File name.
            parent (Directory): Parent directory. Defaults to None.
        """
        
        self.name = name
        self.content = content
        self.parent = parent
        
        self.creation_date = datetime.datetime.now()
        self.last_modified_date = self.creation_date
    
    # Methods -------------------------------------------------------------------
    
    def update_content(self, content: str) -> None:
        """
        Updates the current file content.

        Args:
            content (str): New content string.
        """
        self.content = content
        self.last_modified_date = datetime.datetime.now()
    
    def modify_name(self, new_name: str):
        """
        Changes current file name.

        Args:
            new_name (str): New directory name.
        """
        
        if not self.parent.check_file_existence(new_name):
            self.name = new_name
            self.last_modified_date = datetime.datetime.now()
            return True
        
        return False