class DaoError(Exception):
    """Base exception class for Dao operations related errors."""
    def __init__(self, template_key="generic", message="Exception occurred during dao operation"):
        self.template_key = template_key
        self.message = message

class UserUpdateError(DaoError):
    """Exception raised when an error occurs during user update."""
    def __init__(self, template_key, message="Failed to update the user in the collection"):
        self.message = message
        self.template_key = template_key
        super().__init__(self.template_key, self.message)

class UserDataNotFoundError(DaoError):
    """Exception raised when an error occurs during user update."""
    def __init__(self, template_key, message="Failed to update the user in the collection"):
        self.message = message
        self.template_key = template_key
        super().__init__(self.template_key, self.message)
